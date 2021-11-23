from io import BytesIO
from pathlib import Path
from typing import Union

import geopandas as gpd
import numpy as np
import rasterio
import typer
from rasterio import features
from shapely.geometry import Polygon, shape


def create_footprint(input_file: Union[str, Path, BytesIO]) -> gpd.GeoDataFrame:
    """Create a footprint from an input raster file"""

    with rasterio.open(input_file) as src:
        # Read the first band of the image and the no data mask to numpy arrays
        src_band = src.read(1)
        nodata_msk = src.read_masks(1)
        crs = src.crs

        # Make a numpy array with all valid pixels as 1 (i.e. not "no-data")
        # If we tried to polygonise the src_band directly we would get one geojson
        # feature for each pixel value which is not desired
        dst_band = np.zeros(src_band.shape, dtype=np.int16)
        dst_band[src_band != src.nodata] = 1

        # Polygonise the numpy array. This returns a tuple of the feature (GeoJSON geometry)
        # and the pixel value. Here we keep the first (and only) geojson feature
        geojson, _ = list(features.shapes(dst_band, mask=nodata_msk, transform=src.transform))[0]

    # Convert the polygonised shapes tuple to a GeoDataFrame
    # fill any holes by keeping only the exterior
    geom = Polygon(shape(geojson).exterior.coords)

    # Create a GeoDataFrame of the result so we can write out the GeoJSON without
    # having to use Fiona directly and to do coordinate transforms easily (if needed)
    return gpd.GeoDataFrame({"geometry": [geom]}, crs=crs)


def main(input_file: Path, output_file: Path, output_format: str = "GeoJSON"):
    """Create a footprint vector from a raster

    Parameters
    ----------
    input_file : Path
        Path to input raster
    output_file : Path
        Path to output vector which will contain the footprint of ``input_file``
    output_format : str, optional
        Output format, by default "GeoJSON"
    """
    # Get the GeoDataFrame that contains the footprint
    gdf = create_footprint(input_file=input_file)

    # If the output is GeoJSON it should be in WGS84
    if output_format == "GeoJSON":
        gdf = gdf.to_crs(4326)

    # Write the output geometry
    gdf.to_file(output_file, driver=output_format)


if __name__ == "__main__":
    typer.run(main)
