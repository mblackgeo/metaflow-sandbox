import os
from pathlib import Path

import geopandas as gpd
from geopandas.testing import assert_geodataframe_equal
from shapely.geometry import Polygon

from footprint.footprint import create_footprint, main


def test_footprint(test_dir: str):
    image_path = os.path.join(test_dir, "landsat.tif")
    fp = create_footprint(image_path)
    assert isinstance(fp, gpd.GeoDataFrame)
    assert isinstance(fp.geometry.iloc[0], Polygon)


def test_main(test_dir: str, tmp_path: Path):
    image_path = Path(test_dir) / "landsat.tif"
    output = tmp_path / "out.geojson"

    fp1 = create_footprint(image_path)
    fp2 = gpd.read_file(main(image_path, output_file=output, output_format="GeoJSON"))

    assert_geodataframe_equal(fp1, fp2)
