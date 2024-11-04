from pyomo.environ import Set


def indices(model) -> None:
    """DC OPF Indexing Sets."""
    model.N = Set(doc="Nodes index.")
    model.L = Set(doc="Transmission lines index.")
    model.G = Set(doc="Generators index.")
