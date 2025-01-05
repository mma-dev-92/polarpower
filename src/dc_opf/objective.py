from pyomo.environ import Objective, minimize


def objective(model) -> None:
    """DC OPF Objective."""
    model.obj = Objective(rule=generation_cost, sense=minimize)


def generation_cost(model):
    return sum(model.GenS[g, s] * model.marginal_cost[g, s] for (g, s) in model.GxS)
