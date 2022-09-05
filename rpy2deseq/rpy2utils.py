import rpy2.robjects as _robjects
from rpy2.robjects import (
    pandas2ri as _pandas2ri,
    numpy2ri as _numpy2ri,
    Formula as _Formula
)

from rpy2.robjects.packages import importr as _importr
from rpy2.robjects.conversion import localconverter as _localconverter
from rpy2.rinterface_lib import sexp as _sexp

_vector_types = {
    'str': _robjects.StrVector,
    'float': _robjects.FloatVector,
    'int': _robjects.IntVector,
    'bool': _robjects.BoolVector
}

def _numpy_to_r(p_obj):
    with _localconverter(_robjects.default_converter + _numpy2ri.converter):
        return _robjects.conversion.py2rpy(p_obj)

def _pandas_to_r(
    p_obj,
    as_matrix=False,
    transpose=False
):

    # Convert to an R data.frame
    if not as_matrix:
        with _localconverter(
            _robjects.default_converter + _pandas2ri.converter
        ):
            return _robjects.conversion.py2rpy(
                p_obj if not transpose else p_obj.T
            )

    # Convert to a R matrix with rownames and colnames
    else:
        with _localconverter(
            _robjects.default_converter + _numpy2ri.converter
        ):

            mat = _robjects.conversion.py2rpy(
                p_obj.values if not transpose else p_obj.values.T
            )

            idx_list = p_obj.index.astype(str).tolist()
            col_list = p_obj.columns.astype(str).tolist()

            mat.rownames = _to_vector(
                idx_list if not transpose else col_list
            )

            mat.colnames = _to_vector(
                col_list if not transpose else idx_list
            )

            return mat

def _r_to_numpy(r_obj):
    with _localconverter(
        _robjects.default_converter + _numpy2ri.converter
    ):
        return _robjects.conversion.rpy2py(r_obj)

def _r_to_pandas(r_obj):
    with _localconverter(
        _robjects.default_converter + _pandas2ri.converter
    ):
        return _robjects.conversion.rpy2py(r_obj)

def _r_to_list(r_obj):

    # Return [None] if r_obj is None
    if isinstance(r_obj, _sexp.NULLType):
        return [None]

    # Convert r_obj to a list
    else:
        return list(r_obj)

def _to_vector(sequence, vector_type='str'):
    return _vector_types[vector_type](sequence)
