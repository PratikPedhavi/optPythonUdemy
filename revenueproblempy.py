# REVENUE PROBLEM

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

def run():
    model = pyo.ConcreteModel()

    model.price = pyo.Var(bounds=(50,200))
    model.ncars = pyo.Var(within=Integers, bounds=(0,None))
    
    model.C1 = pyo.Constraint(expr=1001-5*model.price==model.ncars)

    model.obj = pyo.Objective(expr=model.price*model.ncars, sense=maximize)

    opt = SolverFactory('couenne', executable='C:\\couenne\\bin\\couenne.exe')
    opt.solve(model)

    model.pprint()
    print('Price: ', pyo.value(model.price))
    print('Car count: ', pyo.value(model.ncars))
    print('Revenue: ', pyo.value(model.obj))

run()