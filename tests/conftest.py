"""
Visualisation constants
"""

import uuid

import pytest

import viz.database as database
import viz.steps as steps


@pytest.fixture
def workflow():
    """ """
    wf = steps.make_tmp_workflow()
    return wf 


# @pytest.fixture
# def database(workflow):
#     database.setup_database()
#     database.add_step(step=workflow)

