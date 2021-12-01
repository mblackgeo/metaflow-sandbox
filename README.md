# Metaflow Sandbox
A sandbox repository for playing around with Metaflow and creating flows that use GDAL. Also include is an approach to unit testing with Metaflow.

## Installation

Create a new virtual env, install the requirements:

```shell
conda create -n mtflw python=3.8
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Usage

The repository is organised as follows:

* [deploy](/deploy): The Metaflow CloudFormation template for deploying to Amazon Web Services.
* [footprint](/footprint): Contains a function using rasterio/geopandas to generate a [vector outline of raster](/footprint/footprint.py) and additionally a [Flow](/footprint/flow.py) that implements this process in Metaflow, using an extra [`@pip` decorator](/footprint/utils.py) for installing dependencies.
* [tests](/tests): Unit tests (using pytest) for the footprint code and the flow.
* [tutorials](/tutorials): The standard metaflow tutorials. Follow through the guide on the [Metaflow docs](https://docs.metaflow.org/getting-started/tutorials).

Best place to start is to look at the [`footprint.py`](/footprint/footprint.py) code and then [it's tests](tests/test_footprint.py). Following this, there is a [simple flow](/footprint/flow.py) that demonstrates running it with Metaflow, and using the `@pip` decorator for package installation. These can be run locally:

```shell
# run the flow
python footprint/flow.py --environment=conda show
python footprint/flow.py --environment=conda run --input-file /path/to/a/raster.tif

# run the tests and check coverage
pytest --cov footprint
```

Note: the default landsat scene used by the flow is not committed to this repository due to its size, so substitute your own GDAL compatible raster.

The tests show examples of how to test the rasterio/geopandas code using pytest, though probably more interesting is the approach to testing flows. There are details given in the [`test README`](/tests) and a helper [pytest fixture](/tests/conftest.py) for running these tests using subprocess (not elegant, but it's the way Netflix recommend).