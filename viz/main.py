import steps
import tree
import table


def main():
    wf = steps.make_tmp_workflow()
    tree.Tree(wf)
    # tree.print_tree(wf)
    # table.Table(wf)


if __name__ == "__main__":
    main()
