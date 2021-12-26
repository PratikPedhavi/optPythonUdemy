import pyomo.environ as pyo
from pyomo.environ import *
import pandas as pd
from pyomo.opt import SolverFactory

dataGen = pd.read_excel('inputs.xlsx', sheet_name='gen')
dataLoad = pd.read_excel('inputs.xlsx', sheet_name='load')
print(dataGen.head())
print(dataLoad.head())
Ng = len(dataGen)

# model
model = pyo.ConcreteModel()

model.Pg = pyo.Var(range(Ng), bounds=(0,None))
Pg = model.Pg

# cosntraints
pg_sum = sum([Pg[d] for d in dataGen.id])
model.balance = pyo.Constraint(expr= pg_sum == sum(dataLoad.value))

model.cond = pyo.Constraint(expr= Pg[0]+Pg[3] >= dataLoad.value[0])

model.limits = pyo.ConstraintList()
for g in dataGen.id:
    model.limits.add(expr = Pg[g] <= dataGen.limit[g])

# objFun
model.obj = pyo.Objective(expr = sum([Pg[g]*dataGen.cost[g] for g in dataGen.id]))

opt = SolverFactory('glpk')
results = opt.solve(model)

dataGen['Pg'] = [pyo.value(Pg[g]) for g in dataGen.id]

model.pprint()
print(dataGen)
