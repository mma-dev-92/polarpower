from pyomo.environ import Constraint


def constraints(model) -> None:
    """DC OPF Constraints"""
    model.PowerFlowEquation = Constraint(model.L, rule=power_flow_equation)
    model.BalancingEquation = Constraint(model.N, rule=balancing_equation)
    model.SlackNodeEquation = Constraint(rule=slack_node_equation)
    model.PowerGenerationCostDecomposition = Constraint(model.G, rule=power_generation_cost_decomposition)


def power_flow_equation(model, l):
    """Power flow equation."""
    i, j = model.node_fr[l], model.node_to[l]
    return model.Flow[l] == model.B[l] * (model.Theta[i] - model.Theta[j])


def balancing_equation(model, n):
    """Node balancing equation."""
    power_generation = sum(model.Gen[g] for g in model.gen_at_node[n])
    demand = model.demand[n]
    in_power_flow = sum(model.Flow[l] for l in model.lines_in[n])
    out_power_flow = sum(model.Flow[l] for l in model.lines_out[n])
    return power_generation - demand == in_power_flow - out_power_flow


def power_generation_cost_decomposition(model, g):
    """Power generation decomposition into merit order segments."""
    return model.Gen[g] == sum(model.GenS[g, s] for (g, s) in model.G_GxS[g])


def slack_node_equation(model):
    """Setting slack node voltage angle to 0."""
    return model.Theta[model.slack_node] == 0
