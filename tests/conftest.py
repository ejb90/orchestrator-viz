"""
Visualisation constants
"""

import pathlib

import pytest

import viz.steps as steps


@pytest.fixture
def workflow():
    """
    A dummy workflow for testing
    """
    wf = steps.make_tmp_workflow()
    return wf


# @pytest.fixture
# def database(workflow):
#     database.setup_database()
#     database.add_step(step=workflow)


@pytest.fixture
def archive_dir():
    """A directory with a collection of files/directiores to test methods."""
    return pathlib.Path(__file__).resolve().parent / "inputs" / "archive_test_directory"
    