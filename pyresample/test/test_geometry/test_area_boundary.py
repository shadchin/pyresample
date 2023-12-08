#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2023 Pyresample developers
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Test AreaDefinition boundary related methods."""

from unittest.mock import MagicMock
import numpy as np
import pytest
from pyproj import CRS
from pyresample.future.geometry.area import (
    get_full_geostationary_bounding_box_in_proj_coords,
    get_geostationary_angle_extent,
    get_geostationary_bounding_box_in_lonlats,
    get_geostationary_bounding_box_in_proj_coords,
)


@pytest.fixture
def stere_area(create_test_area):
    """Create basic polar-stereographic area definition."""
    proj_dict = {
        'a': '6378144.0',
        'b': '6356759.0',
        'lat_0': '50.00',
        'lat_ts': '50.00',
        'lon_0': '8.00',
        'proj': 'stere'
    }
    shape = (800, 800)
    area_extent = (-1370912.72, -909968.64000000001, 1029087.28, 1490031.3600000001)
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
        attrs={"name": 'areaD'},
    )


@pytest.fixture
def geos_src_area(create_test_area):
    """Create basic geostationary area definition."""
    shape = (3712, 3712)
    area_extent = (-5570248.477339745, -5561247.267842293, 5567248.074173927, 5570248.477339745)
    proj_dict = {'a': 6378169.0, 'b': 6356583.8, 'h': 35785831.0,
                 'lon_0': 0.0, 'proj': 'geos', 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def laea_area(create_test_area):
    """Create basic LAEA area definition."""
    shape = (10, 10)
    area_extent = [1000000, 0, 1050000, 50000]
    proj_dict = {"proj": 'laea', 'lat_0': '60', 'lon_0': '0', 'a': '6371228.0', 'units': 'm'}
    return create_test_area(proj_dict, shape[0], shape[1], area_extent)


@pytest.fixture
def global_lonlat_antimeridian_centered_area(create_test_area):
    """Create global lonlat projection area centered on the -180 antimeridian."""
    shape = (4, 4)
    area_extent = (0, -90.0, 360, 90.0)
    proj_dict = '+proj=longlat +pm=180'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def global_platee_caree_area(create_test_area):
    """Create global platee projection area."""
    shape = (4, 4)
    area_extent = (-180.0, -90.0, 180.0, 90.0)
    proj_dict = 'EPSG:4326'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def global_platee_caree_minimum_area(create_test_area):
    """Create minimum size global platee projection area."""
    """Create global platee projection area."""
    shape = (2, 2)
    area_extent = (-180.0, -90.0, 180.0, 90.0)
    proj_dict = 'EPSG:4326'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def local_platee_caree_area(create_test_area):
    """Create local platee projection area."""
    shape = (4, 4)
    area_extent = (100, 20, 120, 40)
    proj_dict = 'EPSG:4326'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def local_lonlat_antimeridian_centered_area(create_test_area):
    """Create local lonlat projection area centered on the -180 antimeridian."""
    shape = (4, 4)
    area_extent = (100, 20, 120, 40)
    proj_dict = '+proj=longlat +pm=180'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def local_meter_area(create_test_area):
    """Create local meter projection area."""
    shape = (2, 2)
    area_extent = (2_600_000.0, 1_050_000, 2_800_000.0, 1_170_000)
    proj_dict = 'EPSG:2056'
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def south_pole_area(create_test_area):
    """Create projection area centered on south pole."""
    shape = (2, 2)
    area_extent = (-5326849.0625, -5326849.0625, 5326849.0625, 5326849.0625)
    proj_dict = {'proj': 'laea', 'lat_0': -90, 'lon_0': 0, 'a': 6371228.0, 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def north_pole_area(create_test_area):
    """Create projection area centered on north pole."""
    shape = (2, 2)
    area_extent = (-5326849.0625, -5326849.0625, 5326849.0625, 5326849.0625)
    proj_dict = {'proj': 'laea', 'lat_0': 90, 'lon_0': 0, 'a': 6371228.0, 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def geos_fd_area(create_test_area):
    """Create full disc geostationary area definition."""
    shape = (100, 100)
    area_extent = (-5500000., -5500000., 5500000., 5500000.)
    proj_dict = {'a': 6378169.00, 'b': 6356583.80, 'h': 35785831.0,
                 'lon_0': 0, 'proj': 'geos', 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def geos_out_disk_area(create_test_area):
    """Create out of Earth diskc geostationary area definition."""
    shape = (10, 10)
    area_extent = (-5500000., -5500000., -5300000., -5300000.)
    proj_dict = {'a': 6378169.00, 'b': 6356583.80, 'h': 35785831.0,
                 'lon_0': 0, 'proj': 'geos', 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def geos_half_out_disk_area(create_test_area):
    """Create geostationary area definition with portion of boundary out of earth_disk."""
    shape = (100, 100)
    area_extent = (-5500000., -10000., 0, 10000.)
    proj_dict = {'a': 6378169.00, 'b': 6356583.80, 'h': 35785831.0,
                 'lon_0': 0, 'proj': 'geos', 'units': 'm'}
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def geos_conus_area(create_test_area):
    """Create CONUS geostationary area definition (portion is out-of-Earth disk)."""
    shape = (30, 50)  # (3000, 5000) for GOES-R CONUS/PACUS
    proj_dict = {'h': 35786023, 'sweep': 'x', 'x_0': 0, 'y_0': 0,
                 'ellps': 'GRS80', 'no_defs': None, 'type': 'crs',
                 'lon_0': -75, 'proj': 'geos', 'units': 'm'}
    area_extent = (-3627271.29128, 1583173.65752, 1382771.92872, 4589199.58952)
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def geos_mesoscale_area(create_test_area):
    """Create CONUS geostationary area definition."""
    shape = (10, 10)  # (1000, 1000) for GOES-R mesoscale
    proj_dict = {'h': 35786023, 'sweep': 'x', 'x_0': 0, 'y_0': 0,
                 'ellps': 'GRS80', 'no_defs': None, 'type': 'crs',
                 'lon_0': -75, 'proj': 'geos', 'units': 'm'}
    area_extent = (-501004.322, 3286588.35232, 501004.322, 4288596.99632)
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def truncated_geos_area(create_test_area):
    """Create a truncated geostationary area (SEVIRI above 30° lat)."""
    proj_dict = {'a': '6378169', 'h': '35785831', 'lon_0': '9.5', 'no_defs': 'None', 'proj': 'geos',
                 'rf': '295.488065897014', 'type': 'crs', 'units': 'm', 'x_0': '0', 'y_0': '0'}
    area_extent = (5567248.0742, 5570248.4773, -5570248.4773, 1393687.2705)
    shape = (1392, 3712)
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )


@pytest.fixture
def truncated_geos_area_in_space(create_test_area):
    """Create a geostationary area entirely out of the Earth disk !."""
    proj_dict = {'a': '6378169', 'h': '35785831', 'lon_0': '9.5', 'no_defs': 'None', 'proj': 'geos',
                 'rf': '295.488065897014', 'type': 'crs', 'units': 'm', 'x_0': '0', 'y_0': '0'}
    area_extent = (5575000, 5575000, 5570000, 5570000)
    shape = (10, 10)
    return create_test_area(
        proj_dict,
        shape[0],
        shape[1],
        area_extent,
    )




class TestBoundary:
    """Test 'boundary' method for AreaDefinition classes."""

    def test_polar_south_pole_projection(self, south_pole_area):
        """Test boundary for polar projection around the South Pole."""
        areadef = south_pole_area
        boundary = areadef.boundary(force_clockwise=False)

        # Check boundary shape
        height, width = areadef.shape
        n_vertices = (width - 1) * 2 + (height - 1) * 2
        assert boundary.vertices.shape == (n_vertices, 2)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[-45., -55.61313895],
                                      [45., -55.61313895],
                                      [135., -55.61313895],
                                      [-135., -55.61313895]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)

    def test_nort_pole_projection(self, north_pole_area):
        """Test boundary for polar projection around the North Pole."""
        areadef = north_pole_area
        boundary = areadef.boundary(force_clockwise=False)

        # Check boundary shape
        height, width = areadef.shape
        n_vertices = (width - 1) * 2 + (height - 1) * 2
        assert boundary.vertices.shape == (n_vertices, 2)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[-135., 55.61313895],
                                      [135., 55.61313895],
                                      [45., 55.61313895],
                                      [-45., 55.61313895]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)

    def test_geostationary_projection(self, geos_fd_area):
        """Test boundary for geostationary projection."""
        areadef = geos_fd_area

        # Check default boundary shape
        default_n_vertices = 50
        boundary = areadef.boundary(vertices_per_side=None)
        assert boundary.vertices.shape == (default_n_vertices, 2)

        # Check minimum boundary vertices
        n_vertices = 3
        minimum_n_vertices = 4
        boundary = areadef.boundary(vertices_per_side=n_vertices)
        assert boundary.vertices.shape == (minimum_n_vertices, 2)

        # Check odd vertices_per_side number
        # - Rounded to the sequent even number (to construct the sides)
        n_odd_vertices = 5
        boundary = areadef.boundary(vertices_per_side=n_odd_vertices)
        assert boundary.vertices.shape == (n_odd_vertices + 1, 2)

        # Check boundary vertices
        n_vertices = 10
        boundary = areadef.boundary(vertices_per_side=n_vertices, force_clockwise=False)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[-7.54251621e+01, 3.53432890e+01],
                                      [-5.68985178e+01, 6.90053314e+01],
                                      [5.68985178e+01, 6.90053314e+01],
                                      [7.54251621e+01, 3.53432890e+01],
                                      [7.92337283e+01, -0.00000000e+00],
                                      [7.54251621e+01, -3.53432890e+01],
                                      [5.68985178e+01, -6.90053314e+01],
                                      [-5.68985178e+01, -6.90053314e+01],
                                      [-7.54251621e+01, -3.53432890e+01],
                                      [-7.92337283e+01, 6.94302533e-15]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)

    def test_global_platee_caree_projection(self, global_platee_caree_area):
        """Test boundary for global platee caree projection."""
        areadef = global_platee_caree_area
        boundary = areadef.boundary(force_clockwise=False)

        # Check boundary shape
        height, width = areadef.shape
        n_vertices = (width - 1) * 2 + (height - 1) * 2
        assert boundary.vertices.shape == (n_vertices, 2)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[-135., 67.5],
                                      [-45., 67.5],
                                      [45., 67.5],
                                      [135., 67.5],
                                      [135., 22.5],
                                      [135., -22.5],
                                      [135., -67.5],
                                      [45., -67.5],
                                      [-45., -67.5],
                                      [-135., -67.5],
                                      [-135., -22.5],
                                      [-135., 22.5]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)

    def test_minimal_global_platee_caree_projection(self, global_platee_caree_minimum_area):
        """Test boundary for global platee caree projection."""
        areadef = global_platee_caree_minimum_area
        boundary = areadef.boundary(force_clockwise=False)

        # Check boundary shape
        height, width = areadef.shape
        n_vertices = (width - 1) * 2 + (height - 1) * 2
        assert boundary.vertices.shape == (n_vertices, 2)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[-90., 45.],
                                      [90., 45.],
                                      [90., -45.],
                                      [-90., -45.]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)

    def test_local_area_projection(self, local_meter_area):
        """Test local area projection in meter."""
        areadef = local_meter_area
        boundary = areadef.boundary(force_clockwise=False)

        # Check boundary shape
        height, width = areadef.shape
        n_vertices = (width - 1) * 2 + (height - 1) * 2
        assert boundary.vertices.shape == (n_vertices, 2)

        # Check boundary vertices is in correct order
        expected_vertices = np.array([[8.08993639, 46.41074744],
                                      [9.39028624, 46.39582417],
                                      [9.37106733, 45.85619242],
                                      [8.08352612, 45.87097006]])
        np.testing.assert_allclose(expected_vertices, boundary.vertices)


class TestGeostationaryTools:
    """Test the geostationary bbox tools."""

    def test_get_full_geostationary_bbox(self, truncated_geos_area):
        nb_points = 20
        x, y = get_full_geostationary_bounding_box_in_proj_coords(truncated_geos_area, nb_points)
        assert len(x) == nb_points
        assert len(y) == nb_points

        assert x[0] != x[-1]
        assert y[0] != y[-1]

        expected_x = np.array([-5.43062255e+06, -5.16482897e+06, -4.39346593e+06, -3.19203985e+06,
                               -1.67815466e+06, 3.32529726e-10, 1.67815466e+06, 3.19203985e+06,
                               4.39346593e+06, 5.16482897e+06, 5.43062255e+06, 5.16482897e+06,
                               4.39346593e+06, 3.19203985e+06, 1.67815466e+06, 3.32529726e-10,
                               -1.67815466e+06, -3.19203985e+06, -4.39346593e+06, -5.16482897e+06])

        expected_y = np.array([6.62789871e-10, 1.67242779e+06, 3.18114670e+06, 4.37847280e+06,
                               5.14720348e+06, 5.41209002e+06, 5.14720348e+06, 4.37847280e+06,
                               3.18114670e+06, 1.67242779e+06, -0.00000000e+00, -1.67242779e+06,
                               -3.18114670e+06, -4.37847280e+06, -5.14720348e+06, -5.41209002e+06,
                               -5.14720348e+06, -4.37847280e+06, -3.18114670e+06, -1.67242779e+06])

        np.testing.assert_allclose(x, expected_x)
        np.testing.assert_allclose(y, expected_y)

    def test_get_geostationary_bbox_works_with_truncated_area(self, truncated_geos_area):
        """Ensure the geostationary bbox works when truncated."""
        lon, lat = get_geostationary_bounding_box_in_lonlats(truncated_geos_area, 20)

        expected_lon = np.array(
            [-64.24072434653284, -68.69662326361153, -65.92516214783112, -60.726360278290336,
             -47.39851775032484, 9.500000000000018, 66.39851775032487, 79.72636027829033,
             84.92516214783113, 87.69662326361151, 83.24072434653286])
        expected_lat = np.array(
            [14.554922655532085, 17.768795771961937, 35.34328897185421, 52.597860701318254, 69.00533141646078,
             79.1481121862375, 69.00533141646076, 52.597860701318254, 35.34328897185421, 17.768795771961933,
             14.554922655532085])
        np.testing.assert_allclose(lon, expected_lon)
        np.testing.assert_allclose(lat, expected_lat)

    def test_get_geostationary_bbox_works_with_truncated_area_proj_coords(self, truncated_geos_area):
        """Ensure the geostationary bbox works when truncated."""
        x, y = get_geostationary_bounding_box_in_proj_coords(truncated_geos_area, 20)

        expected_x = np.array(
            [-5209128.302753595, -5164828.965702432, -4393465.934674804, -3192039.8468840676, -1678154.6586309497,
             3.325297262895822e-10, 1678154.6586309501, 3192039.846884068, 4393465.934674805, 5164828.965702432,
             5209128.302753594])
        expected_y = np.array(
            [1393687.2705, 1672427.7900638399, 3181146.6955466354, 4378472.798117005, 5147203.47659387,
             5412090.016106332, 5147203.476593869, 4378472.798117005, 3181146.695546635, 1672427.7900638392,
             1393687.2705])

        np.testing.assert_allclose(x, expected_x)
        np.testing.assert_allclose(y, expected_y)

    def test_get_geostationary_bbox_does_not_contain_inf(self, truncated_geos_area):
        """Ensure the geostationary bbox does not contain np.inf."""
        lon, lat = get_geostationary_bounding_box_in_lonlats(truncated_geos_area, 20)
        assert not any(np.isinf(lon))
        assert not any(np.isinf(lat))

    def test_get_geostationary_bbox_returns_empty_lonlats_in_space(self, truncated_geos_area_in_space):
        """Ensure the geostationary bbox is empty when in space."""
        lon, lat = get_geostationary_bounding_box_in_lonlats(truncated_geos_area_in_space, 20)

        assert len(lon) == 0
        assert len(lat) == 0

    def test_get_geostationary_bbox(self):
        """Get the geostationary bbox."""
        geos_area = MagicMock()
        lon_0 = 0
        proj_dict = {'a': 6378169.00,
                     'b': 6356583.80,
                     'h': 35785831.00,
                     'lon_0': lon_0,
                     'proj': 'geos'}
        geos_area.crs = CRS(proj_dict)
        geos_area.area_extent = [-5500000., -5500000., 5500000., 5500000.]

        lon, lat = get_geostationary_bounding_box_in_lonlats(geos_area, 20)
        expected_lon = np.array([-78.19662326, -75.42516215, -70.22636028,
                                 -56.89851775, 0., 56.89851775, 70.22636028,
                                 75.42516215, 78.19662326, 79.23372832, 78.19662326,
                                 75.42516215, 70.22636028, 56.89851775, 0.,
                                 -56.89851775, -70.22636028, -75.42516215, -78.19662326, -79.23372832, ])
        expected_lat = np.array([17.76879577, 35.34328897, 52.5978607,
                                 69.00533142, 79.14811219, 69.00533142, 52.5978607,
                                 35.34328897, 17.76879577, -0., -17.76879577,
                                 -35.34328897, -52.5978607, -69.00533142, -79.14811219,
                                 -69.00533142, -52.5978607, -35.34328897, -17.76879577, 0.])

        np.testing.assert_allclose(lon, expected_lon, atol=1e-07)
        np.testing.assert_allclose(lat, expected_lat, atol=1e-07)

        geos_area = MagicMock()
        lon_0 = 10
        proj_dict = {'a': 6378169.00,
                     'b': 6356583.80,
                     'h': 35785831.00,
                     'lon_0': lon_0,
                     'proj': 'geos'}
        geos_area.crs = CRS(proj_dict)
        geos_area.area_extent = [-5500000., -5500000., 5500000., 5500000.]

        lon, lat = get_geostationary_bounding_box_in_lonlats(geos_area, 20)
        np.testing.assert_allclose(lon, expected_lon + lon_0)

    def test_get_geostationary_angle_extent(self):
        """Get max geostationary angles."""
        geos_area = MagicMock()
        proj_dict = {
            'proj': 'geos',
            'sweep': 'x',
            'lon_0': -89.5,
            'a': 6378169.00,
            'b': 6356583.80,
            'h': 35785831.00,
            'units': 'm'}
        geos_area.crs = CRS(proj_dict)

        expected = (0.15185342867090912, 0.15133555510297725)
        np.testing.assert_allclose(expected,
                                   get_geostationary_angle_extent(geos_area))

        proj_dict['a'] = 1000.0
        proj_dict['b'] = 1000.0
        proj_dict['h'] = np.sqrt(2) * 1000.0 - 1000.0
        geos_area.crs = CRS(proj_dict)

        expected = (np.deg2rad(45), np.deg2rad(45))
        np.testing.assert_allclose(expected,
                                   get_geostationary_angle_extent(geos_area))

        proj_dict = {
            'proj': 'geos',
            'sweep': 'x',
            'lon_0': -89.5,
            'ellps': 'GRS80',
            'h': 35785831.00,
            'units': 'm'}
        geos_area.crs = CRS(proj_dict)
        expected = (0.15185277703584374, 0.15133971368991794)
        np.testing.assert_allclose(expected,
                                   get_geostationary_angle_extent(geos_area))