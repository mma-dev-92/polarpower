from math import pi

from pyomo.environ import Reals  # type: ignore
from pyomo.environ import Var


def variables(model) -> None:
    """DC OPF Optimization Variables."""
    generator_variables(model)
    transmission_line_variables(model)
    node_variables(model)


def generator_variables(model) -> None:
    """Generator variables for the DC OPF optimization problem."""
    model.Gen = Var(
        model.G,
        within=Reals,
        bounds=lambda model, g: (model.pmin[g], model.pmax[g]),
        doc="Generation [per unit] at each generator.",
    )


def transmission_line_variables(model) -> None:
    """Transmission line variables for the DC OPF optimization problem."""
    model.Flow = Var(
        model.L,
        within=Reals,
        bounds=lambda model, l: (model.fmin[l], model.fmax[l]),
        doc="Power flow [per unit] on transmission lines.",
    )


def node_variables(model) -> None:
    """Node variables for the DC OPF optimization problem."""
    model.Theta = Var(
        model.N, within=Reals, bounds=(0.0, 2 * pi), doc="Voltage angle at each node."
    )
