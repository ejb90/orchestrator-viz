"""
Visualisation constants
"""

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
