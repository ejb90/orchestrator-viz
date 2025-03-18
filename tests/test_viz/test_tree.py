""" 
Test Tree view
"""

import pytest

import viz.database as database
import viz.steps as steps
import viz.tree as tree


@pytest.mark.parametrize(
    ("source", "path", "key"),
    [
        ("db", "test.db", "uuid"),
        ("db", "test.db", "path"),
        ("pkl", "test.pkl", "uuid"),
        ("pkl", "test.pkl", "path"),
        #  ("json", "test.json", "uuid"),
        #  ("json", "test.json", "path"),
    ],
)
def test_tree(tmp_path, workflow, source, path, key):
    """
    Test tree print successfully builds for different inputs
    """
    if source == "db":
        # Database
        fname = f"{database.RDBMS}:///{tmp_path / path}"
        database.setup_database(fname)
        database.add_step(db_path=fname, step=workflow)
    elif source == "pkl":
        # Pickle
        fname = tmp_path / path
        steps.dump_workflow_pickle(workflow, fname)
    elif source == "json":
        # JSON
        fname = tmp_path / path
        steps.dump_workflow_json(workflow, fname)

    # set both to string
    if key == "uuid":
        value = workflow.uuid.hex
    elif key == "path":
        value = str(workflow.path)

    tree.main(
        argv=["--source", source, "--fname", str(tmp_path / path), f"--{key}", value]
    )
