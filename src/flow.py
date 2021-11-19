from io import BytesIO

from metaflow import FlowSpec, IncludeFile, Parameter, conda, conda_base, step

from flow_utils import pip


def script_path(filename):
    import os

    filepath = os.path.join(os.path.dirname(__file__))
    return os.path.join(filepath, filename)


@conda_base(python="3.8.12")
class RasterFootprintFlow(FlowSpec):
    """
    Generate a vector file containing the footprint of a raster.
    """

    input_file = IncludeFile(
        "input_file",
        help="Input raster image to generate a footprint for.",
        default=script_path("data/landsat.tif"),
        is_text=False,
    )

    @step
    def start(self):
        """
        Start step.
        """
        print("Creating footprint")
        self.next(self.process)

    @conda(libraries={"gdal": "3.0.2"})
    @pip(libraries={"rasterio": "1.2.10", "geopandas": "0.10.2", "typer[all]": "0.4.0"})
    @step
    def process(self):
        """
        Create the footprint of the raster
        """
        from footprint import create_footprint

        gdf = create_footprint(input_file=BytesIO(self.input_file))
        self.footprint = gdf.to_crs(4326).to_json(drop_id=True)

        self.next(self.end)

    @step
    def end(self):
        """
        End step.
        """
        print("Created footprint")


if __name__ == "__main__":
    RasterFootprintFlow()
