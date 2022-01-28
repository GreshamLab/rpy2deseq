# Inspired by https://github.com/wckdouglas/diffexpr
from rpy2deseq.rpy2utils import _importr, _robjects, _r_to_list, _r_to_numpy, _pandas_to_r, _r_to_pandas, _Formula
import numpy as _np
import pandas as _pd


class DESeq2:
    
    deseq = _importr('DESeq2')
    bp = _importr('BiocParallel')
    to_dataframe = _robjects.r('function(x) data.frame(x)')
    
    threads = 1
    
    def __init__(self, count_data, meta_data, design_formula, threads=1):
        """
        DESeq2 wrapper written in rpy2
        
        :param count_data: Samples x Genes dataframe
        :type count_data: pd.DataFrame
        """
        self.gene_names = count_data.columns.copy()
        self.sample_names = count_data.index.copy()
        self.count_matrix, self.design_matrix, self.formula = self._deseq_to_r(count_data, meta_data, design_formula)
        self.threads = threads
        
    def run(self, **kwargs):
        self.de_obj = self._execute_deseq(self.count_matrix, self.design_matrix, self.formula, self.threads, **kwargs)
        return self
        
    def results(self, contrast, lfcThreshold=0, **kwargs):
        results = self._return_results(self.de_obj, contrast, lfcThreshold=lfcThreshold, **kwargs)
        results.index = self.gene_names
        return results
    
    def multiresults(self, contrast_func, contrast_iter, contrast_col, **kwargs):
        multires = []
        for x in contrast_iter:
            res = self.results(contrast_func(x), **kwargs)
            res[contrast_col] = x
            multires.append(res)
        return _pd.concat(multires)
    
    def results_names(self):
        return list(self.deseq.resultsNames(self.de_obj))

    @staticmethod
    def _deseq_to_r(count_data, meta_data, design_formula):
        
        count_matrix = _pandas_to_r(count_data, as_matrix=True, transpose=True)       
        design_matrix = _pandas_to_r(meta_data)
        formula = _Formula(design_formula)

        return count_matrix, design_matrix, formula

    @classmethod
    def _execute_deseq(cls, r_count, r_meta, r_design, threads=1, **kwargs):
        dds = cls.deseq.DESeqDataSetFromMatrix(countData=r_count, 
                                               colData=r_meta,
                                               design=r_design)
        return cls.deseq.DESeq(dds, BPPARAM=cls.bp.MulticoreParam(workers=threads), **kwargs)

    @classmethod
    def _return_results(cls, r_deseq, contrast, lfcThreshold=0.0, **kwargs):

        deseq_result = cls.deseq.results(r_deseq, contrast=_robjects.StrVector(contrast), lfcThreshold=float(lfcThreshold), **kwargs)
        return _r_to_pandas(cls.to_dataframe(deseq_result))

        
        