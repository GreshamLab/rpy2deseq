# Inspired by https://github.com/wckdouglas/diffexpr

from rpy2deseq.rpy2utils import (
    _importr,
    _robjects,
    _pandas_to_r,
    _r_to_pandas,
    _Formula)

import pandas as _pd


class DESeq2:

    deseq = _importr('DESeq2')
    bp = _importr('BiocParallel')
    to_dataframe = _robjects.r('function(x) data.frame(x)')

    count_rows_are_genes = False
    threads = 1

    gene_names = None
    sample_names = None

    def __init__(
        self,
        count_data,
        meta_data,
        design_formula,
        threads=1,
        count_rows_are_genes=False
    ):
        """
        DESeq2 wrapper written in rpy2

        :param count_data: Samples x enes dataframe
        :type count_data: pd.DataFrame
        """
        self.gene_names = count_data.columns.copy()
        self.sample_names = count_data.index.copy()
        self.count_matrix, self.design_matrix, self.formula = self._deseq_to_r(
            count_data,
            meta_data,
            design_formula,
            transpose=not count_rows_are_genes
        )

        self.threads = threads

    def run(self, **kwargs):
        """
        Create a DESeqDataSet using DESeqDataSetFromMatrix
        and then call DESeq on it for diffrential expression

        :param **kwargs: Keyword arguments for DESeq
        :return: This DESeq2 instance
        :rtype: DESeq2
        """

        self.de_obj = self._execute_deseq(
            self.count_matrix,
            self.design_matrix,
            self.formula,
            self.threads,
            **kwargs
        )

        return self

    def results(
        self,
        contrast,
        lfcThreshold=0,
        **kwargs
    ):
        """
        Get results for a specific contrasting comparison

        :param contrast: A tuple (Variable, Compare_To_Value, Compare_From_Value)
            to build results. E.g. ("Time", "30", "0") etc.
        :type contrast: tuple
        :param lfcThreshold: Log FC null threshold,
            defaults to 0
        :type lfcThreshold: int, optional
        :return: Dataframe with DESeq2 results indexed by gene
        :rtype: pd.DataFrame
        """

        results = self._return_results(
            self.de_obj,
            contrast,
            lfcThreshold=lfcThreshold,
            **kwargs
        )

        results.index = self.gene_names
        return results

    def multiresults(
        self,
        contrast_func,
        contrast_iter,
        contrast_col,
        **kwargs
    ):
        """
        Get dataframe with multiple comparison results

        :param contrast_func: A function that is mapped onto
            contrast_iter to generate a comparison tuple as used by
            .results(). E.g. lambda x: ("Time", x, "0")
        :type contrast_func: callable
        :param contrast_iter: An iterable of values to feed into
            contrast_func to generate comparison tuples as used by
            .results(). E.g. ["30", "60", "90"]
        :type contrast_iter: iterable
        :param contrast_col: Dataframe column to store the value from
            contrast_iter for each comparison. E.g. "Time"
        :type contrast_col: str
        :return: Dataframe with multiple DESeq2 results
        :rtype: pd.DataFrame
        """

        multires = []

        for x in contrast_iter:

            # Get results for a single comparison
            res = self.results(
                contrast_func(x),
                **kwargs
            )

            # Create the coomparison value column and fill it
            res[contrast_col] = x
            multires.append(res)

        return _pd.concat(multires)

    def results_names(self):
        """
        Get resultsNames from DESeq2 object

        :return: Result names
        :rtype: list
        """
        return list(self.deseq.resultsNames(self.de_obj))

    @staticmethod
    def _deseq_to_r(
        count_data,
        meta_data,
        design_formula,
        transpose=False
    ):

        # Make the count matrix
        count_matrix = _pandas_to_r(
            count_data,
            as_matrix=True,
            transpose=transpose
        )

        # Make the design metadata matrix
        design_matrix = _pandas_to_r(
            meta_data
        )

        # Convert the formula string to an R formula object
        formula = _Formula(design_formula)

        return count_matrix, design_matrix, formula

    @classmethod
    def _execute_deseq(
        cls,
        r_count,
        r_meta,
        r_design,
        threads=1,
        **kwargs
    ):
        # Make the DESeqDataSet
        dds = cls.deseq.DESeqDataSetFromMatrix(
            countData=r_count,
            colData=r_meta,
            design=r_design
        )

        # Execute and return DESeq2 object
        return cls.deseq.DESeq(
            dds,
            BPPARAM=cls.bp.MulticoreParam(workers=threads),
            **kwargs
        )

    @classmethod
    def _return_results(
        cls,
        r_deseq,
        contrast,
        lfcThreshold=0.0,
        **kwargs
    ):

        deseq_result = cls.deseq.results(
            r_deseq,
            contrast=_robjects.StrVector(contrast),
            lfcThreshold=float(lfcThreshold),
            **kwargs
        )

        return _r_to_pandas(cls.to_dataframe(deseq_result))
