"""
Table visualisation of workflow
"""

import sys

import rich.console
import rich.table

import viz.settings as settings
import viz.steps as steps


COLUMN2COLUMNTITLE = {
    "name": "Name",
    "status": "Status",
    "path": "Path",
    "uuid": "UUID",
    "ctime": "Creation Time",
    "mtime": "Modification Time",
    "scheduler": "Scheduler",
}


class Table:
    """
    Show the Workflow in Table view

    Attrs:
        wf (workflow.Workflow):         workflow.Workflow instance
    """

    def __init__(self, wf, columns=None, options=settings.Settings()):
        """
        Initialise table

        Args:
            wf (workflow.Workflow):         workflow.Workflow instance
            columns (list):                 List of column names to print
            options (settings.Settings)     Visualisation options

        Returns:
            None
        """
        self.wf = wf
        self._columns = columns if columns is not None else options.columns
        self._settings = options

        self.initialise_table()
        self.build_table(self.wf.steps)
        self.print()

    def initialise_table(self):
        """
        Initialse rich.Table object

        Args:

        Returns:
            None
        """
        self.table = rich.table.Table(title=self.wf.name)
        for column in self._columns:
            self.table.add_column(COLUMN2COLUMNTITLE[column])

    def print(self):
        """
        Print the table

        Args:

        Returns:
            None
        """
        console = rich.console.Console(color_system=self._settings.colour)
        console.print(self.table)

    def build_table(self, stps):
        """
        For a given (sub)workflow, add rows to the table for each step
        If the step is a workflow, call this function iteratively

        Args:
            stps (list):        List of Step instances

        Returns:
            None
        """
        for step in stps:
            rows = []
            for column in self._columns:
                if column == "status":
                    rows.append(f"[{settings.STATUS2COLOUR[step.status]}]{step.status}")
                elif column == "uuid":
                    rows.append(step.uuid.hex)
                elif column in ("ctime", "mtime"):
                    rows.append(getattr(step, column).strftime("%Y-%m-%d %H:%M:%S"))
                elif column == 'scheduler':
                    rows.append(step.scheduler.table if step.scheduler else None)
                else:
                    rows.append(str(getattr(step, column)))

            self.table.add_row(*rows)

            if isinstance(step, steps.Workflow):
                self.build_table(step.steps)


def main(argv=sys.argv[1:]):
    """
    Args:
        argv (list):        List of arguments (for pytest compatability)

    Returns:
        None
    """
    # import viz.database as database
    # wf = steps.make_tmp_workflow()
    # database.setup_database()
    # database.add_step(step=wf)
    # print(wf.uuid)

    args = settings.get_args(argv)
    wf = settings.load_wf(args)
    Table(wf)


if __name__ == "__main__":
    main()
