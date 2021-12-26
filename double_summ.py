import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

def firstrule(model,t):
    return 2*model.X[2,t] - 8*model.X[3,t] <= 0


model = pyo.ConcreteModel()

### Parameters and Sets
model.m = pyo.Param(initialize=4, mutable=True)
machine_max = model.m

model.T = pyo.Param(initialize=10)
time_max = model.T

model.setM = pyo.RangeSet(1,model.m)  # range(1,machine_max+1)
machines = model.setM
model.setT = pyo.RangeSet(1,model.T)    # range(1,time_max+1)
timeslots = model.setT

model.X = pyo.Var(model.setM, model.setT, within=Integers, bounds=(0,10))

X = model.X

model.C1 = pyo.Constraint(model.setT, rule=firstrule)


# model.C1 = pyo.ConstraintList()
# for t in model.setT:
#     model.C1.add(expr=2*X[2,t] - 8*X[3,t] <= 0)

model.C2 = pyo.ConstraintList()
for t in range(3,time_max+1):
    model.C2.add(expr=X[2,t] - 2*X[3,t-2] + X[4,t] >= 1)

model.C3 = pyo.ConstraintList()
for t in model.setT:
    model.C3.add(expr=sum([X[m,t] for m in model.setM]) <=50)

model.C4 = pyo.ConstraintList()
for t in range(2,time_max+1):
    model.C4.add(expr=X[1,t] + X[2,t-1] + X[3,t] + X[4,t] <= 10)

model.C5 = pyo.ConstraintList()
for m in model.setM:
    for t in model.setT:
        model.C5.add(expr=pyo.inequality(0,X[m,t],10))

# model.obj = pyo.Objective(expr=sum([X[m,t] for m in machines for t in timeslots]), sense=maximize)
model.obj = pyo.Objective(expr=pyo.summation(X), sense=maximize)

model.m = pyo.Param(initialize=5, mutable=True)

opt = SolverFactory('glpk')
# opt = SolverFactory('Ipopt', executable='C:\\Ipopt\\bin\\ipopt.exe')
# opt.options['MIPgap'] = 0.03
results = opt.solve(model, tee=True)

model.pprint()
# for m in machines:
#     for t in timeslots:
#         print('X [{0},{1}] = {2}'.format(m,t,pyo.value(X[m,t])))

print('Objective = ', pyo.value(model.obj))
