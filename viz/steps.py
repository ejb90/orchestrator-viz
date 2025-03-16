"""
These are a series of dummy functions to mimic a real workflow from Orchestrator
"""

import datetime
import pathlib
import pickle
import random
import uuid



STATUS = [
    "unstarted",
    "pending",
    "running",
    "completed",
    "failed",
]


class Step:
    """ """

    def __init__(self, name, status):
        """ """
        self.name = name
        self.status = status
        self.path = pathlib.Path().resolve() / self.name
        self.uuid = uuid.uuid4()
        self.ctime = datetime.datetime.now()
        self.mtime = datetime.datetime.now()


class Task(Step):
    """ """

    def __init__(self, name, status):
        """ """
        super().__init__(name, status)


class Workflow(Step):
    """ """

    def __init__(self, name, status="unstarted", steps=[]):
        """ """
        super().__init__(name, status)
        self.steps = steps

    def fix_paths(self):
        """ """
        for step in self.steps:
            step.path = self.path / step.name.replace(" ", "_").lower()


def make_tmp_workflow():
    """
    Make a temp tree to loop through
    """
    steps = [
        "step 1",
        "step 2",
        "step 3",
        "step 4",
        "step 5",
    ]
    models = [
        "model A",
        "model B",
        "model C",
        "model D",
        "model E",
    ]

    wf = Workflow("main")

    for model in models:
        tasks = []
        for step in steps:
            tasks.append(Task(step, STATUS[random.randint(0, 4)]))
        wf.steps.append(
            Workflow(model, steps=tasks, status=STATUS[random.randint(0, 4)])
        )
        wf.steps[-1].fix_paths()
    wf.fix_paths()

    wf.steps[2].steps.append(Task("new step", status="unstarted"))

    with open("status.pkl", "wb") as fobj:
        pickle.dump(wf, fobj)
    
    return wf


def load_workflow_pickle(fname):
    """
    Load workflow from pickle file
    """
    with open(fname, "rb") as fobj:
        obj = pickle.load(fobj)
    return obj


if __name__ == "__main__":
    make_tmp_workflow()