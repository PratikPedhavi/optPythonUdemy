import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import time

model = pyo.ConcreteModel()

model.x = pyo.Var(bounds = (-np.inf,3))
model.y = pyo.Var(bounds = (0,np.inf))

x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= x+y<=8)
model.C2 = pyo.Constraint(expr= 8*x+3*y>=-24)
model.C3 = pyo.Constraint(expr= -6*x+8*y<=48)
model.C4 = pyo.Constraint(expr= 3*x+5*y<=15)

model.Obj = pyo.Objective(expr= -4*x-2*y, sense=minimize)

tempo_initial = time.time()
opt = SolverFactory('glpk')
# opt = SolverFactory('cbc', executable='C:\\cbc\\bin\\cbc.exe')
opt.solve(model)
tempo = time.time() - tempo_initial

model.pprint()

print('Runtime ',tempo)
print('x = ', pyo.value(x))
print('y = ', pyo.value(y))
