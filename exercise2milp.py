import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np

model = pyo.ConcreteModel()

model.x = pyo.Var(range(5), within=Integers, bounds=(0,np.inf))
model.y = pyo.Var(bounds=(0,np.inf))

x = model.x
y = model.y

sum_x = sum([x[k] for k in range(5)])
model.C1 = pyo.Constraint(expr=sum_x+y<=20)

model.C2 = pyo.ConstraintList()
for k in range(5):
    model.C2.add(expr=x[k]+y>=15)

model.C3 = pyo.Constraint(expr=sum([(k+1)*x[k] for k in range(5)]) >=10)

model.C4 = pyo.Constraint(expr=x[4]+2*y>=30)

model.obj = pyo.Objective(expr=sum_x+y, sense=minimize)

model.pprint()

# opt = SolverFactory('glpk')
opt = SolverFactory('cbc', executable='C:\\cbc\\bin\\cbc.exe')
results = opt.solve(model)

print(results)

print('Value of X: ')
print([pyo.value(x[k]) for k in range(5)])

print('Value of Y: ')
print(pyo.value(y))

print('Obj: ', pyo.value(model.obj))
