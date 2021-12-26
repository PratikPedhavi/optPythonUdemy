import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

def firstrule(model,t):
    return 2*model.X[2,t] - 8*model.X[3,t] <= 0
def secondrule(model,t):
    return model.X[2,t] - 2*model.X[3,t-2] + model.X[4,t] >= 1
def thirdrule(model,t):
    return sum([model.X[m,t] for m in model.setM]) <=50
def fourthrule(model,t):
    return model.X[1,t] + model.X[2,t-1] + model.X[3,t] + model.X[4,t] <= 10
def fifthrule(model,m,t):
    return pyo.inequality(0,model.X[m,t],10)

def run():
    model = pyo.ConcreteModel()
    ### Parameters and Sets
    model.m = pyo.Param(initialize=4, mutable=True)
    model.T = pyo.Param(initialize=10)
    model.setM = pyo.RangeSet(1,model.m)
    model.setT = pyo.RangeSet(1,model.T)
    ### Variables
    model.X = pyo.Var(model.setM, model.setT, within=Integers, bounds=(0,10))
    ### Consttraints
    model.C1 = pyo.Constraint(model.setT, rule=firstrule)
    model.C2 = pyo.Constraint(range(3,model.T+1), rule=secondrule)
    model.C3 = pyo.Constraint(model.setT, rule=thirdrule)
    model.C4 = pyo.Constraint(range(2,model.T+1), rule=fourthrule)
    model.C5 = pyo.Constraint(model.setM, model.setT, rule=fifthrule)
    ### Objective
    model.obj = pyo.Objective(expr=pyo.summation(model.X), sense=maximize)
    ### Solver
    opt = SolverFactory('glpk')
    results = opt.solve(model, tee=True)

    model.pprint()
    print('Objective = ', pyo.value(model.obj))

run()
