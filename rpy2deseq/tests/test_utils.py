import unittest
import numpy as np
import pandas as pd
import numpy.testing as npt
import pandas.testing as pdt

from rpy2deseq.rpy2utils import (_numpy_to_r, _r_to_numpy, _pandas_to_r, _r_to_pandas, _r_to_list, _to_vector)


NUMPY_ARRAY = np.random.rand(100).reshape(20, 5)


class TestNumpyR(unittest.TestCase):

    def setUp(self):
        self.arr = NUMPY_ARRAY.copy()
        self.df = pd.DataFrame(self.arr)


    def test_np_to_r_and_back(self):
        r_obj = _numpy_to_r(self.arr)
        array_back = _r_to_numpy(r_obj)

        npt.assert_array_equal(self.arr, array_back)
        npt.assert_array_equal(self.arr, NUMPY_ARRAY)


    def test_pd_to_r_and_back(self):
        r_obj = _pandas_to_r(self.df)
        df_back = _r_to_pandas(r_obj)

        pdt.assert_index_equal(self.df.index.astype(str), df_back.index)
        pdt.assert_index_equal(self.df.columns.astype(str), df_back.columns)
        npt.assert_almost_equal(df_back.values, NUMPY_ARRAY)
        npt.assert_almost_equal(self.df.values, NUMPY_ARRAY)


    def test_pd_to_r_and_back_to_np(self):
        r_obj = _pandas_to_r(self.df, as_matrix=True)
        array_back = _r_to_numpy(r_obj)

        npt.assert_almost_equal(array_back, NUMPY_ARRAY)
        npt.assert_almost_equal(self.df.values, NUMPY_ARRAY)        

    def test_pd_to_r_and_back_to_np_t(self):
        r_obj = _pandas_to_r(self.df, as_matrix=True, transpose=True)
        array_back = _r_to_numpy(r_obj)

        npt.assert_almost_equal(array_back, NUMPY_ARRAY.T)
        npt.assert_almost_equal(self.df.values, NUMPY_ARRAY)        

    def test_vectors(self):
        arr = np.arange(10)

        r_obj = _to_vector(arr, vector_type='int')
        ints_back = _r_to_list(r_obj)

        npt.assert_array_equal(arr, np.array(ints_back))
