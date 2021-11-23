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
    output_path = tmp_path / "out.geojson"

    # Run the main function to generate the output file
    main(image_path, output_file=str(output_path), output_format="GeoJSON")

    # check the result of the main and the create_footprint function are identical
    fp1 = create_footprint(image_path).to_crs(epsg=4326)
    fp2 = gpd.read_file(str(output_path))
    assert_geodataframe_equal(fp1, fp2, check_less_precise=True)
