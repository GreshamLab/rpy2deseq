import rpy2.robjects as _robjects
from rpy2.robjects import pandas2ri as _pandas2ri, numpy2ri as _numpy2ri, Formula as _Formula
from rpy2.robjects.conversion import localconverter as _localconverter
from rpy2.robjects.packages import importr as _importr
from rpy2.rinterface_lib import sexp as _sexp

def _numpy_to_r(p_obj):
    with _localconverter(_robjects.default_converter + _numpy2ri.converter):
        return _robjects.conversion.py2rpy(p_obj)

def _pandas_to_r(p_obj, as_matrix=False, transpose=False):
    if not as_matrix:
        with _localconverter(_robjects.default_converter + _pandas2ri.converter):
            return _robjects.conversion.py2rpy(p_obj if not transpose else p_obj.T)
    else:
        with _localconverter(_robjects.default_converter + _numpy2ri.converter):
            mat = _robjects.conversion.py2rpy(p_obj.values if not transpose else p_obj.values.T)
            mat.rownames = _robjects.StrVector(p_obj.index.tolist() if not transpose else p_obj.columns.tolist())
            mat.colnames = _robjects.StrVector(p_obj.columns.tolist() if not transpose else p_obj.index.tolist())
            return mat
            
def _r_to_numpy(r_obj):
    with _localconverter(_robjects.default_converter + _numpy2ri.converter):
        return _robjects.conversion.rpy2py(r_obj)    

def _r_to_pandas(r_obj):
    with _localconverter(_robjects.default_converter + _pandas2ri.converter):
        return _robjects.conversion.rpy2py(r_obj)

def _r_to_list(r_obj):
    return [None] if isinstance(r_obj, _sexp.NULLType) else list(r_obj)
