from pyomo.environ import AbstractModel

from src.dc_opf.constraints import constraints
from src.dc_opf.objective import objective
from src.dc_opf.parameters import parameters
from src.dc_opf.sets import indices
from src.dc_opf.variables import variables
from src.model.power_system_model import PowerSystemModel


def df_opf_abstract_model():
    """Symbolic DC OPF Optimization Model Implementation."""
    opt_model = AbstractModel()
    indices(opt_model)
    parameters(opt_model)
    variables(opt_model)
    constraints(opt_model)
    objective(opt_model)
    return opt_model


def dc_opf(power_system_model: PowerSystemModel) -> None:
    """Solve DC OPF on given PowerSystemModel object."""
    # TODO: create ConcreteModel from an AbstractModel based on the
    #   given power_system_model
    # TODO: run the optimization problem and update the system state
    #   from the model results
    # TODO: If model is infeasible, raise an error indicating, that
    #   computation crushed
    pass
