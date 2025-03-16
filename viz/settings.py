"""
"""
import argparse
import json
import pathlib
import pickle

import viz.steps as steps


STATUS2COLOUR = {
    "unstarted": "grey62",
    "pending": "purple",
    "running": "blue",
    "completed": "green",
    "failed": "red",
}


def get_args():
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
    parser = argparse.ArgumentParser(description='CLI options for visualisation')

    parser.add_argument(
        '-s',
        '--source', 
        type=str,
        default='db',
        choices=["db", "json", "pkl"],
        help='Path at the start of the workflow'
        )
     
    parser.add_argument(
        '-d',
        '--database', 
        type=pathlib.Path,
        # default=database.DATABASE,
        default=pathlib.Path("orchestrator.db"),
        help='Path at the start of the workflow'
        )
    
    parser.add_argument(
        '-p', 
        '--pickle',
        type=pathlib.Path,
        default=None,
        help='Location of the pickle status file'
        )
    
    parser.add_argument(
        '-j', 
        '--json',
        type=pathlib.Path,
        default=None,
        help='Location of the JSON status file'
        )
    
    parser.add_argument(
        '-u', 
        '--uuid',
        type=str,
        default=None,
        help='UUID of the start of the workflow'
        )
    
    parser.add_argument(
        '-q', 
        '--path',
        type=pathlib.Path,
        default=None,
        )
    
    # Parse arguments
    args = parser.parse_args()
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
        if not args.database.is_file():
            raise Exception(f"Database at \"{args.database}\" not found")
        if args.uuid is not None:
            pass
            # database.get(args.database, args.uuid)
        elif args.path is not None:
            # query database based on path name
            pass

    # Secondary method - use the pickle file, loop through top level
    elif args.source == "pkl":
        if not args.pickle.is_file():
            raise Exception(f"Pickle file at \"{args.pickle}\" not found")
        obj = steps.load_workflow_pickle(args.pickle)
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
        if not args.database.is_file():
            raise Exception(f"JSON file at \"{args.json}\" not found")
        with open(args.pickle, "r") as fobj:
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
        raise Exception(f"Workflow source \"{args.source}\" not recognised")

    # Raise exception if nothing is found
    if workflow is None:
        raise Exception("No worklow found with given options")
    return workflow
