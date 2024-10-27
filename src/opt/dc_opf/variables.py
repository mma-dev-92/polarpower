from pyomo.core import NonNegativeReals  # type: ignore
from pyomo.environ import Var


def define_variables(model) -> None:
    """DC OPF Optimization Variables."""
    model.gen = Var(
        model.G, within=NonNegativeReals, doc="Generation at each generator."
    )
    model.theta = Var(model.N, doc="Voltage angle at each node.")
    model.pflow = Var(model.B, doc="Power flow on each branch.")
