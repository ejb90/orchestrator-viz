import pathlib

import click
import rich.console
import rich.table

import viz.settings as settings
import viz.steps as steps


COLUMNS = [
    "name",
    "status",
    "path",
    "uuid",
    "ctime",
    "mtime",
]
COLUMN2COLUMNTITLE = {
    "name": "Name",
    "status": "Status",
    "path": "Path",
    "uuid": "UUID",
    "ctime": "Creation Time",
    "mtime": "Modification Time",
}


class Table:
    """ 
    Show the Workflow in Table view
    """

    def __init__(self, wf, columns=COLUMNS):
        """
        Initialise table

        Args:
            wf (workflow.Workflow):         workflow.Workflow instance
            columns (list):                 List of column names to print 
        """
        self.wf = wf
        self.columns = columns
        
        self.initialise_table()
        self.build_table(self.wf.steps)
        self.print()
    
    def initialise_table(self):
        """
        Initialse rich.Table object
        """
        self.table = rich.table.Table(title=self.wf.name)
        for column in self.columns:
            self.table.add_column(COLUMN2COLUMNTITLE[column])

    def print(self):
        """ 
        Print the table
        
        Args:
        
        Returns:
            None
        """
        console = rich.console.Console()
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
            for column in self.columns:
                if column == "status":
                    rows.append(f'[{settings.STATUS2COLOUR[step.status]}]{step.status}')
                elif column == "uuid":
                    rows.append(step.uuid.hex)
                elif column in ("ctime", "mtime"):
                    rows.append(getattr(step, column).strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    rows.append(str(getattr(step, column)))

            self.table.add_row(*rows)

            if isinstance(step, steps.Workflow):
                self.build_table(step.steps)



def main():
    """ """
    args = settings.get_args()
    wf = settings.load_wf(args)
    Table(wf)


if __name__ == "__main__":
    main()
