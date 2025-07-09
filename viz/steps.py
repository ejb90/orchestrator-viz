"""
These are a series of dummy functions to mimic a real workflow from Orchestrator
"""

import datetime
import pathlib
import pickle
import random
import uuid

import viz.database as database


STATUS = [
    "unstarted",
    "pending",
    "running",
    "failed",
    "completed",
]


class Scheduler:
    """
    Scheduler object

    Attrs:
        type (str):         Scheduler type
        partition (str):    Partition type
        nodes (int):        Number of nodes
        ppn (int):          Number of procs per node
        procs (int):        Total number of procs
        wallclock (int):    Wallclock [s]
    """

    def __init__(self):
        """
        Initialise Scheduler

        Args:

        Returns:
            None
        """
        self.type = "slurm"
        self.partition = "parallel"
        self.nodes = 1
        self.ppn = 1
        self.procs = 1
        self.wallclock = 1
        self.wallclock_remaining = None
        self.wallclock_expired = None

    @property
    def table(self):
        """
        Print scheduler in table format

        Args:

        Returns:
            None
        """
        string = f"{self.type}-{self.partition}: {self.nodes}n*{self.ppn}ppn\n"
        string += f"Requested WC: {self.wallclock}\n"
        string += f"Current WC: {self.wallclock_expired}\n"
        string += f"Remaining WC: {self.wallclock_remaining}"
        return string


class Step:
    """
    Step base instance

    Attrs:
        name (str):                 Step name
        status (str):               Step status
        steps (list):               List of steps
        path (pathlib.Path):        Root path of Step
        uuid (uuid.UUID):           UUID
        ctime (datetime.datetime):  Creation time
        mtime (datetime.datetime):  Modification time
        scheduler (scheduler):      Scheduler object
    """

    def __init__(self, name, status):
        """
        Initialise Step

        Args:
            name (str):         Step name
            status (str):       Step status

        Returns:
            None
        """
        self.name = name
        self.status = status
        self.path = pathlib.Path().resolve() / self.name.replace(" ", "_").lower()
        self.uuid = uuid.uuid4()
        self.ctime = datetime.datetime.now()
        self.mtime = datetime.datetime.now()
        self.scheduler = None
        self.parent_flow_type = "serial"


class Task(Step):
    """
    Task instance

    Attrs:
        name (str):                 Task name
        status (str):               Task status
        steps (list):               List of steps
        path (pathlib.Path):        Root path of task
        uuid (uuid.UUID):           UUID
        ctime (datetime.datetime):  Creation time
        mtime (datetime.datetime):  Modification time
        scheduler (scheduler):      Scheduler object
    """

    def __init__(self, name, status):
        """
        Initialise Task

        Args:
            name (str):         Task name
            status (str):       Task status

        Returns:
            None
        """
        super().__init__(name, status)
        self.type = "task"

class Workflow(Step):
    """
    Workflow instance

    Attrs:
        name (str):                 Workflow name
        status (str):               Workflow status
        steps (list):               List of steps
        path (pathlib.Path):        Root path of workflow
        uuid (uuid.UUID):           UUID
        ctime (datetime.datetime):  Creation time
        mtime (datetime.datetime):  Modification time
        scheduler (scheduler):      Scheduler object
    """

    def __init__(self, name, status="unstarted", steps=[]):
        """
        Initialise workflow

        Args:
            name (str):         Workflow name
            status (str):       Workflow status
            steps (list):       List of steps

        Returns:
            None
        """
        super().__init__(name, status)
        self.steps = steps
        self.flow_type = 'serial'
        self.type = "workflow"

    def fix_paths(self):
        """
        Fix paths relative to parent

        Args:

        Returns:
            None
        """
        for step in self.steps:
            step.path = self.path / step.name.replace(" ", "_").lower()


# ========================================================================================================================
# Tmp to mimic suite
# ========================================================================================================================
def make_tmp_task(name, status):
    """
    Build a temp task

    Args:
        name (str):         Task name
        status (str):       Task status
    """
    scheduler = Scheduler()
    scheduler.partition = "parallel" if name == "step 3" else "serial"
    scheduler.nodes = 4 if name == "step 3" else 1
    scheduler.ppn = 64 if name == "step 3" else 1
    scheduler.procs = scheduler.nodes * scheduler.ppn

    task = Task(name, status)
    task.scheduler = scheduler

    return task


def make_tmp_workflow():
    """
    Make a temp tree to loop through

    Args:
        None

    Returns:
        wf (workflow.Workflow):         Temp workflow object
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
        status = None
        for step in steps:
            roll = random.randint(0, 19)
            if roll < 15 and status in (None, "completed"):
                status = "completed"
            else:
                roll = random.randint(0, 3)
                status = STATUS[roll]
            tasks.append(make_tmp_task(step, status))
        wf.steps.append(
            Workflow(
                model,
                steps=tasks,
                status="completed"
                if all([t.status == "completed" for t in tasks])
                else "failed",
            )
        )
        wf.steps[-1].fix_paths()

    wf.fix_paths()

    wf.steps[2].steps.append(Task("new step", status="unstarted"))
    return wf


def dump_workflow_pickle(obj, fname):
    """
    Dump workflow to pickle file
    """
    with open(fname, "wb") as fobj:
        pickle.dump(obj, fobj)


def load_workflow_pickle(fname):
    """
    Load workflow from pickle file
    """
    with open(fname, "rb") as fobj:
        obj = pickle.load(fobj)
    return obj


def add_steps_iteratively(wf):
    database.add_step(step=wf)
    for step in wf.steps:
        if step.type == "workflow":
            add_steps_iteratively(step)
        else:
            database.add_step(step=step)

def main():
    """Dump tmp workflow."""
    wf = make_tmp_workflow()
    database.setup_database()
    add_steps_iteratively(wf)
    # print(wf.uuid)



if __name__ == "__main__":
    main()