from pypamguard import load_pamguard_binary_file
from pypamguard.core.pgbfile import PGBFile
from pypamguard.base import BaseChunk
from pypamguard.utils.serializer import serialize
from pypamguard.core.filters import Filters, DateFilter, RangeFilter, WhitelistFilter, BaseFilter
from pypamguard.logger import Verbosity
import os, json
import pytest
from ._constants import TESTS

@pytest.fixture
def filters():
    return Filters()

def _test_chunk(chunk: BaseChunk, test_data: dict, test_name, chunk_name):
    chunk_json: dict = chunk.to_json()
    for attr, expected in test_data.items():
        assert attr in chunk_json, f"Test {test_name}: chunk '{chunk_name}' does not have attribute '{attr}'"
        data = chunk_json[attr]
        assert data == expected, f"Test {test_name}: chunk '{chunk_name}' attribute '{attr}' has unexpected value: expected {expected} ({type(expected)}), got {data} ({type(data)})"

def _get_paths(test_metadata):
    directory = os.path.join(test_metadata["directory"], test_metadata["filename"])
    json_path = os.path.join(test_metadata["directory"], test_metadata["json"])
    pgdf_path = f"{directory}.pgdf"
    pgdx_path = f"{directory}.pgdx"
    pgnf_path = f"{directory}.pgnf"
    assert os.path.exists(json_path)
    assert os.path.exists(pgdf_path)
    # assert os.path.exists(pgdx_path)
    # assert os.path.exists(pgnf_path)
    return directory, json_path, pgdf_path, pgdx_path, pgnf_path

def _get_json_data(json_path):
    with open(json_path, "r") as f:
        json_data = json.loads(f.read())
        assert "file_header" in json_data, "Test data is missing 'file_header'"
        assert "module_header" in json_data, "Test data is missing 'module_header'"
        assert "module_footer" in json_data, "Test data is missing 'module_footer'"
        assert "file_footer" in json_data, "Test data is missing 'file_footer'"
        assert "data" in json_data, "Test data is missing 'data'"
        return json_data

def _run_header_tests(file: PGBFile, json_data, test_name):
    _test_chunk(file.file_header, json_data["file_header"], test_name, "file_header")
    _test_chunk(file.module_header, json_data["module_header"], test_name, "module_header")

def _run_footer_tests(file: PGBFile, json_data, test_name):
    _test_chunk(file.module_footer, json_data["module_footer"], test_name, "module_footer")
    _test_chunk(file.file_footer, json_data["file_footer"], test_name, "file_footer")

def _run_data_tests(file: PGBFile, json_data, test_name):
    json_data_len = len(json_data["data"])
    assert len(file.data) == len(json_data["data"]), f"Test {test_name}: data length mismatch: expected {json_data_len}, got {len(file.data)}"
    for index, json_chunk in enumerate(json_data["data"]):
        _test_chunk(file.data[index], json_chunk, test_name, f"data[{index}]")

def _run_pgdf_tests(file: PGBFile, json_data, test_name):
    _run_header_tests(file, json_data, test_name)
    _run_footer_tests(file, json_data, test_name)
    _run_data_tests(file, json_data, test_name)

def _run_pgnf_tests(file: PGBFile, json_data, test_name):
    _run_header_tests(file, json_data, test_name)
    _run_footer_tests(file, json_data, test_name)

def get_filters(test_data, filters):
    filters_json = test_data["filters"]
    for filter in filters_json:
        filters.add(filter, BaseFilter.from_json(filters_json[filter]))
    return filters

@pytest.mark.parametrize("test_data", TESTS, ids=[os.path.join(x["directory"], x["json"]) for x in TESTS])
def test_module(test_data, filters):    
    directory, json_path, pgdf_path, pgdx_path, pgnf_path = _get_paths(test_data)
    json_data = _get_json_data(json_path)
    get_filters(json_data, filters)
    file_pgdf = load_pamguard_binary_file(pgdf_path, verbosity=Verbosity.WARNING, filters=filters)   
    assert isinstance(file_pgdf, PGBFile)
    _run_pgdf_tests(file_pgdf, json_data, json_path)