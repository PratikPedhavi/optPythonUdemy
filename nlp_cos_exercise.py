import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(initialize=1, bounds=(-5,5))
model.y = pyo.Var(initialize=1, bounds=(-5,5))

x = model.x
y = model.y

model.obj = pyo.Objective(expr=cos(x+1)+cos(x)*cos(y))

model.pprint()

opt = SolverFactory('ipopt', executable='C:\\Ipopt\\bin\\ipopt.exe')
results = opt.solve(model)

print(results)

print('x ', pyo.value(x))
print('y ', pyo.value(y))
print('obj ', pyo.value(model.obj))
