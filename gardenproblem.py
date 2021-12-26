# GARDEN PROBLEM

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import  SolverFactory

def perimeter(model,x,y):
    return 2*x+y<=100

def run():
    model = pyo.ConcreteModel()
    
    model.x = pyo.Var(bounds=(0,None))
    model.y = pyo.Var(bounds=(0,None))

    model.C1 = pyo.Constraint(expr=2*model.x+model.y<=100)

    model.obj = pyo.Objective(expr=model.x*model.y,sense=maximize)

    # opt = SolverFactory('glpk', executable='C:\\glpk-4.65\\w64\\glpsol.exe')
    opt = SolverFactory('couenne', executable='C:\\couenne\\bin\\couenne.exe')
    opt.solve(model)

    model.pprint()
    print('Objective = ', pyo.value(model.obj))
    print('x :',pyo.value(model.x))
    print('y :',pyo.value(model.y))

run()
