""" """

import argparse
import json
import pathlib
import uuid

import viz.database as database
import viz.steps as steps


STATUS2COLOUR = {
    "unstarted": "grey62",
    "pending": "purple",
    "running": "blue",
    "completed": "green",
    "failed": "red",
}


# === TO REPLACE WITH core.Settings instance ==============================================
class Settings:
    """
    Output settings

    This should just be the core.Settings class eventually

    Attrs:
        TODO
    """

    def __init__(self, fname="settings.yaml"):
        """ """
        self.columns = [
            "name",
            "status",
            "path",
            "uuid",
            "ctime",
            "mtime",
            # "scheduler",
        ]
        self.colour = "standard"
# === TO REPLACE WITH core.Settings instance ==============================================


def get_args(argv):
    """
    CLI args for visualisation

    Ways to get a workflow:
    1. Database + UUID
    2. Database + path (potentially non-unique!)
    3. Pickle + UUID
    4. Pickle + path (potentially non-unique!)
    5. JSON + UUID
    5. JSON + path (potentially non-unique!)

    Args:

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="CLI options for visualisation")

    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="db",
        choices=["db", "json", "pkl"],
        help="Path at the start of the workflow",
    )

    parser.add_argument(
        "-f",
        "--fname",
        type=pathlib.Path,
        default=database.DATABASE,
        help="Path to the status object (DB/Pickle/JSON)",
    )

    parser.add_argument(
        "-u",
        "--uuid",
        type=str,
        default=None,
        help="UUID of the start of the workflow",
    )

    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        default=None,
    )

    # Parse arguments
    args = parser.parse_args(argv)

    if isinstance(args.uuid, str):
        args.uuid = uuid.UUID(args.uuid)

    return args


def load_wf(args):
    """
    Load workflow, based on user input

    Args:
        args (argparse.Namespace):          Arguments

    Return:
        wf (workflow.Workflow):             Workflow
    """
    workflow = None

    # In order preference, db, pkl, json, unless explicit

    # Main database method - query via UUID or path trivially as it's flat
    if args.source == "db":
        if not args.fname.is_file():
            raise Exception(f'Database at "{args.fname}" not found')
        if args.uuid is not None:
            workflow = database.query_step_by_uuid(
                db_path=f"{database.RDBMS}:///{args.fname}", uuid=args.uuid
            )
        elif args.path is not None:
            workflow = database.query_step_by_path(
                db_path=f"{database.RDBMS}:///{args.fname}", path=str(args.path)
            )

    # Secondary method - use the pickle file, loop through top level
    elif args.source == "pkl":
        if not args.fname.is_file():
            raise Exception(f'Pickle file at "{args.fname}" not found')
        obj = steps.load_workflow_pickle(args.fname)
        if args.uuid is not None:
            if obj.uuid == args.uuid:
                workflow = obj
            else:
                for step in obj.steps:
                    if step.uuid == args.uuid:
                        workflow = step
        elif args.path is not None:
            if obj.path == args.path:
                workflow = obj
            else:
                for step in obj.steps:
                    if step.path == args.path:
                        workflow = step
        else:
            workflow = obj

    # Secondary method - use the JSON file, loop through top level
    elif args.source == "json":
        if not args.fname.is_file():
            raise Exception(f'JSON file at "{args.fname}" not found')
        with open(args.fname, "r") as fobj:
            obj = json.load(fobj)
        if args.uuid is not None:
            if obj.uuid == args.uuid:
                workflow = obj
            else:
                for step in obj.steps:
                    if step.uuid == args.uuid:
                        workflow = step
        elif args.path is not None:
            if obj.path == args.path:
                workflow = obj
            else:
                for step in obj.steps:
                    if step.path == args.path:
                        workflow = step
        else:
            workflow = obj

    # Catch other source types
    else:
        raise Exception(f'Workflow source "{args.source}" not recognised')

    # Raise exception if nothing is found
    if workflow is None:
        raise Exception("No worklow found with given options")
    return workflow
