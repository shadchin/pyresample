import sys
import logging
import numpy as np
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

LOG = logging.getLogger(__name__)


def create_test_longitude(start, stop, shape, twist_factor=0.0, dtype=np.float32):
    if start > stop:
        stop += 360.0

    lon_row = np.linspace(start, stop, num=shape[1]).astype(dtype)
    twist_array = np.arange(shape[0]).reshape((shape[0], 1)) * twist_factor
    lon_array = np.repeat([lon_row], shape[0], axis=0)
    lon_array += twist_array

    if stop > 360.0:
        lon_array[lon_array > 360.0] -= 360
    return lon_array


def create_test_latitude(start, stop, shape, twist_factor=0.0, dtype=np.float32):
    lat_col = np.linspace(start, stop, num=shape[0]).astype(dtype).reshape((shape[0], 1))
    twist_array = np.arange(shape[1]) * twist_factor
    lat_array = np.repeat(lat_col, shape[1], axis=1)
    lat_array += twist_array
    return lat_array


dynamic_wgs84 = {
    "grid_name": "test_wgs84_fit",
    "origin_x": None,
    "origin_y": None,
    "width": None,
    "height": None,
    "cell_width": 0.0057,
    "cell_height": -0.0057,
    "proj4_definition": "+proj=latlong +datum=WGS84 +ellps=WGS84 +no_defs",
}

static_lcc = {
    "grid_name": "test_lcc",
    "origin_x": -1950510.636800,
    "origin_y": 4368587.226913,
    "width": 5120,
    "height": 5120,
    "cell_width": 1015.9,
    "cell_height": -1015.9,
    "proj4_definition": "+proj=lcc +a=6371200 +b=6371200 +lat_0=25 +lat_1=25 +lon_0=-95 +units=m +no_defs",
}


class TestLL2CRStatic(unittest.TestCase):
    def test_lcc_basic1(self):
        from pyresample.ewa import _ll2cr
        lon_arr = create_test_longitude(-95.0, -75.0, (50, 100), dtype=np.float64)
        lat_arr = create_test_latitude(18.0, 40.0, (50, 100), dtype=np.float64)
        grid_info = static_lcc.copy()
        fill_in = np.nan
        proj_str = grid_info["proj4_definition"]
        cw = grid_info["cell_width"]
        ch = grid_info["cell_height"]
        ox = grid_info["origin_x"]
        oy = grid_info["origin_y"]
        w = grid_info["width"]
        h = grid_info["height"]
        points_in_grid = _ll2cr.ll2cr_static(lon_arr, lat_arr, fill_in, proj_str,
                                                               cw, ch, w, h, ox, oy)
        self.assertEqual(points_in_grid, lon_arr.size, "all these test points should fall in this grid")

    def test_lcc_fail1(self):
        from pyresample.ewa import _ll2cr
        lon_arr = create_test_longitude(-15.0, 15.0, (50, 100), dtype=np.float64)
        lat_arr = create_test_latitude(18.0, 40.0, (50, 100), dtype=np.float64)
        grid_info = static_lcc.copy()
        fill_in = np.nan
        proj_str = grid_info["proj4_definition"]
        cw = grid_info["cell_width"]
        ch = grid_info["cell_height"]
        ox = grid_info["origin_x"]
        oy = grid_info["origin_y"]
        w = grid_info["width"]
        h = grid_info["height"]
        points_in_grid = _ll2cr.ll2cr_static(lon_arr, lat_arr, fill_in, proj_str,
                                             cw, ch, w, h, ox, oy)
        self.assertEqual(points_in_grid, 0, "none of these test points should fall in this grid")


class TestLL2CRDynamic(unittest.TestCase):
    def test_latlong_basic1(self):
        from pyresample.ewa import _ll2cr
        lon_arr = create_test_longitude(-95.0, -75.0, (50, 100), dtype=np.float64)
        lat_arr = create_test_latitude(15.0, 30.0, (50, 100), dtype=np.float64)
        grid_info = dynamic_wgs84.copy()
        fill_in = np.nan
        proj_str = grid_info["proj4_definition"]
        cw = grid_info["cell_width"]
        ch = grid_info["cell_height"]
        ox = grid_info["origin_x"]
        oy = grid_info["origin_y"]
        w = grid_info["width"]
        h = grid_info["height"]
        points_in_grid, lon_res, lat_res, ox, oy, w, h = _ll2cr.ll2cr_dynamic(lon_arr, lat_arr, fill_in, proj_str,
                                                                              cw, ch, w, h, ox, oy)
        self.assertEqual(points_in_grid, lon_arr.size, "all points should be contained in a dynamic grid")
        self.assertIs(lon_arr, lon_res)
        self.assertIs(lat_arr, lat_res)
        self.assertEqual(lon_arr[0, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")
        self.assertEqual(lat_arr[-1, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")

    def test_latlong_basic2(self):
        from pyresample.ewa import _ll2cr
        lon_arr = create_test_longitude(-95.0, -75.0, (50, 100), twist_factor=0.6, dtype=np.float64)
        lat_arr = create_test_latitude(15.0, 30.0, (50, 100), twist_factor=-0.1, dtype=np.float64)
        grid_info = dynamic_wgs84.copy()
        fill_in = np.nan
        proj_str = grid_info["proj4_definition"]
        cw = grid_info["cell_width"]
        ch = grid_info["cell_height"]
        ox = grid_info["origin_x"]
        oy = grid_info["origin_y"]
        w = grid_info["width"]
        h = grid_info["height"]
        points_in_grid, lon_res, lat_res, ox, oy, w, h = _ll2cr.ll2cr_dynamic(lon_arr, lat_arr, fill_in, proj_str,
                                                                              cw, ch, w, h, ox, oy)
        self.assertEqual(points_in_grid, lon_arr.size, "all points should be contained in a dynamic grid")
        self.assertIs(lon_arr, lon_res)
        self.assertIs(lat_arr, lat_res)
        self.assertEqual(lon_arr[0, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")
        self.assertEqual(lat_arr[-1, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")

    def test_latlong_dateline1(self):
        from pyresample.ewa import _ll2cr
        lon_arr = create_test_longitude(165.0, -165.0, (50, 100), twist_factor=0.6, dtype=np.float64)
        lat_arr = create_test_latitude(15.0, 30.0, (50, 100), twist_factor=-0.1, dtype=np.float64)
        grid_info = dynamic_wgs84.copy()
        fill_in = np.nan
        proj_str = grid_info["proj4_definition"]
        cw = grid_info["cell_width"]
        ch = grid_info["cell_height"]
        ox = grid_info["origin_x"]
        oy = grid_info["origin_y"]
        w = grid_info["width"]
        h = grid_info["height"]
        points_in_grid, lon_res, lat_res, ox, oy, w, h = _ll2cr.ll2cr_dynamic(lon_arr, lat_arr, fill_in, proj_str,
                                                                              cw, ch, w, h, ox, oy)
        self.assertEqual(points_in_grid, lon_arr.size, "all points should be contained in a dynamic grid")
        self.assertIs(lon_arr, lon_res)
        self.assertIs(lat_arr, lat_res)
        self.assertEqual(lon_arr[0, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")
        self.assertEqual(lat_arr[-1, 0], 0, "ll2cr returned the wrong result for a dynamic latlong grid")
        self.assertTrue(np.all(np.diff(lon_arr[0]) >= 0), "ll2cr didn't return monotonic columns over the dateline")

