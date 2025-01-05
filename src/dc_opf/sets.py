from pyomo.environ import Set


def indices(model) -> None:
    """DC OPF Indexing Sets."""
    model.N = Set(doc="Nodes index.")
    model.L = Set(doc="Transmission lines index.")
    model.G = Set(doc="Generators index.")

    model.GxS = Set(dimen=2, doc="(Generator, Segments) pairs.")
    model.G_GxS = Set(model.G, within=model.GxS, doc="g -> {(g, s): (g, s) in GxS}")
