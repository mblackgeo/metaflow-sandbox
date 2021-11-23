import os
from io import StringIO

import geopandas as gpd
from metaflow import Flow


def test_flow_show(runner: "CliRunner", flow_dir: str):
    # This test does not actually execute the flow but checks that it compiles
    # correctly and returns an exit code of zero
    proc = runner.run(["flow.py", "--environment", "conda", "show"], flow_dir=flow_dir)
    assert proc.returncode == 0


def test_flow_run(runner: "CliRunner", flow_dir: str, test_dir: str):
    # Run the flow with a small image
    # TODO - make sure this works
    proc = runner.run(
        ["flow.py", "--environment", "conda", "run" "--input-file", os.path.join(test_dir, "landsat.tif")],
        flow_dir=flow_dir,
    )
    assert proc.returncode == 0

    # use the client api to check the output
    run = Flow("RasterFootprintFlow").latest_run
    assert run.successful

    # check there is a geojson file returned in the flow
    result = gpd.read_file(StringIO(run.data.footprint))
    assert result is not None
