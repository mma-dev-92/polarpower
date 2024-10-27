from pyomo.environ import AbstractModel
from src.model.power_system_model import PowerSystemModel
from src.opt.dc_opf.constraints import define_constraints
from src.opt.dc_opf.objective import define_objective
from src.opt.dc_opf.parameters import define_parameters
from src.opt.dc_opf.sets import define_sets
from src.opt.dc_opf.variables import define_variables


def df_opf_abstract_model():
    """Symbolic DC OPF Optimization Model Implementation."""
    opt_model = AbstractModel()
    define_sets(opt_model)
    define_parameters(opt_model)
    define_variables(opt_model)
    define_constraints(opt_model)
    define_objective(opt_model)
    return opt_model


def dc_opf(power_system_model: PowerSystemModel):
    """Solve DC OPF on given PowerSystemModel object."""
    pass
