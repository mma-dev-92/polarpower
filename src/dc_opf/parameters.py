from pyomo.environ import Param, PositiveReals, Reals  # type: ignore


def parameters(model) -> None:
    """DC OPF Paramters"""
    node_parameters(model)
    generator_parameters(model)
    transmission_line_parameters(model)


def node_parameters(model) -> None:
    """Node parameters for the DC OPF optimization problem."""
    model.demand = Param(
        model.N, within=Reals, doc="Power demand [per unit] at each node."
    )
    model.gen_at_node = Param(
        model.N, within=model.G, doc="Generators attached to a node."
    )
    model.lines_in = Param(
        model.N, within=model.L, doc="List of inflow transmission lines."
    )
    model.lines_out = Param(
        model.N, within=model.L, doc="List of outflow transmission lines."
    )
    model.slack_node = Param(within=model.N)


def generator_parameters(model) -> None:
    """Generator parameters for the DC OPF optimization problem."""
    model.pmax = Param(
        model.G, within=Reals, doc="Maximum generation capacity [per unit]."
    )
    model.pmin = Param(
        model.G, within=Reals, doc="Minimum generation capacity [per unit]."
    )


def transmission_line_parameters(model) -> None:
    """Transmission line parameters for the DC OPF optimization problem."""
    model.fmax = Param(
        model.L,
        within=Reals,
        doc="Maximum power flow on a transmission line [per unit].",
    )
    model.fmin = Param(
        model.L,
        within=Reals,
        doc="Minimum power flow on a transmission line [per unit].",
    )
    model.subsceptance = Param(
        model.L, within=PositiveReals, doc="Transmission line subsceptance [per unit]."
    )
    model.node_fr = Param(model.L, within=model.N, doc="Starting node of a line.")
    model.node_to = Param(model.L, within=model.N, doc="End node of a line.")


def transformer_parameters(model) -> None:
    """Transformer parameters for the DC OPF optimization problem."""
    raise NotImplementedError("Transformers are not supported yet.")
