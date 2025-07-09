"""
Tree visualisation of workflow
"""

import sys
import rich
import rich.layout
import rich.tree

import viz.settings as settings
import viz.steps as steps


class Tree:
    """
    Show the Workflow in Tree view

    Attrs:
        wf (workflow.Workflow):         workflow.Workflow instance
        tree (rich.tree.Tree):          rich.tree.Tree instance
    """

    def __init__(self, wf, options=settings.Settings()):
        """
        Initialise Tree

        Args:
            wf (workflow.Workflow):         workflow.Workflow instance

        Returns:
            None
        """
        self.wf = wf
        self.settings = options

        self.initialise_tree()
        self.tree = self.build_tree(self.wf, self.tree)
        self.print(self.tree)

    def initialise_tree(self):
        """
        Initialise tree instance

        Args:

        Returns:
            None
        """
        self.tree = rich.tree.Tree(self.wf.name)

    def build_tree(self, wf, tree):
        """
        Iteratively build the workflow tree

        Args:
            wf (workflow.Workflow):         workflow.Workflow instance
            tree (rich.tree.Tree):          initial Tree instance

        Returns:
            tree (rich.tree.Tree):          updated Tree instance

        """
        for step in wf.steps:
            branch = tree.add(f"[{settings.STATUS2COLOUR[step.status]}]{step.name}")
            if isinstance(step, steps.Workflow):
                self.build_tree(step, branch)
        return tree
    
    def build_legend(self):
        """
        Add legend describing the colour/bold info
        """
        table = rich.table.Table(title="Legend")
        table.add_column("Format")
        table.add_column("Description")

        table.add_row(f"[bold]Colours[/bold]")
        for status, colour in settings.STATUS2COLOUR.items():
            table.add_row(f"[{colour}]{colour}[/{colour}]", status)
        table.add_row(f"")
        table.add_row(f"[bold]Format[/bold]")
        table.add_row(f"[italic]italic[/italic]", "Parallel")
        table.add_row(f"standard", "Serial")
        
        return table

    def print(self, wf):
        """
        Print the Table view to console

        Args:
            wf (workflow.Workflow):         workflow.Workflow instance

        Returns:
            None
        """
        layout = rich.layout.Layout()

        layout.split_row(
            rich.layout.Layout(name="tree"),
            rich.layout.Layout(name="legend"),
        )

        layout["tree"].ratio = 2

        layout["tree"].update(self.tree)
        layout["legend"].update(self.build_legend())

        console = rich.console.Console(color_system=self.settings.colour)
        console.print(layout, crop=True)


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
    Tree(wf)


if __name__ == "__main__":
    main()
