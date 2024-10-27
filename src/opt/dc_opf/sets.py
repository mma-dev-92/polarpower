from pyomo.environ import Set


def define_sets(model) -> None:
    """DC OPF Indexing Sets."""
    model.N = Set(doc="Nodes index.")
    model.B = Set(doc="Branches index.")
    model.G = Set(doc="Generators index.")
