from metaflow import FlowSpec, Parameter, conda, conda_base, step


def script_path(filename):
    import os

    filepath = os.path.join(os.path.dirname(__file__))
    return os.path.join(filepath, filename)


@conda_base(python="3.7")
class RasterFootprintFlow(FlowSpec):
    """
    Generate a vector file containing the footprint of a raster.
    """

    input_file = Parameter(
        "input_file", help="Input raster image to generate a footprint for.", default=script_path("landsat.tif")
    )

    output_file = Parameter(
        "output_file",
        help="Output vector containing the footprint of the input.",
        default=script_path("footprint.geojson"),
    )

    output_format = Parameter(
        "output_format",
        help="Format of the output footprint.",
        default="GeoJSON",
    )

    @step
    def start(self):
        """
        Start step.
        """
        print(
            f"Creating footprint file : {self.output_file} ({self.output_format}), from input image : {self.input_file}"
        )
        self.next(self.process)

    @conda(libraries={"rasterio": "1.2.10", "geopandas": "0.10.2"})
    @step
    def process(self):
        """
        Create the footprint of the raster
        """
        from footprint import create_footprint

        create_footprint(input_file=self.input_file, output_file=self.output_format, output_format=self.output_format)
        self.next(self.end)

    @step
    def end(self):
        """
        End step.
        """
        print(
            f"Created footprint file : {self.output_file} ({self.output_format}), from input image : {self.input_file}"
        )


if __name__ == "__main__":
    RasterFootprintFlow()
