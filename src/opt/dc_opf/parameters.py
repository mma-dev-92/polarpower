from pyomo.environ import Param


def define_parameters(model) -> None:
    """DC OPF Paramters"""
    model.demand = Param(model.N, doc="Power demand at each node.")
    model.fmin = Param(model.B, doc="Minimum power flow on each branch.")
    model.fmax = Param(model.B, doc="Maximum power flow on each branch.")
    model.subsceptance = Param(model.B, doc="Branch subsceptance.")
    model.incidence = Param(model.B, model.N, doc="Branch-node incidence matrix.")
    model.pmax = Param(model.G, doc="Maximum generation capacity.")
    model.pmin = Param(model.G, doc="Minimum generation capacity.")
    model.tap_ratio = Param(model.B, doc="Branch tap ratio.")
    model.phase_shift = Param(model.B, doc="Branch phase shift.")
