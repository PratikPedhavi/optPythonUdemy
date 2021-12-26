import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

def run():
    model = pyo.ConcreteModel()

    file = pd.ExcelFile('.\\Inputs\\route_exercise_inputs.xlsx')
    print('Sheet Names: ', file.sheet_names)
    nodes = file.parse('nodes')
    paths = file.parse('paths')
    print(nodes)
    print(paths)
    nodes = nodes.set_index('node')
    nVars = len(paths)

    model.routes = pyo.Var(range(nVars),within=Binary)
    origin = nodes[nodes.description == 'origin'].index
    destination = nodes[nodes.description == 'destination'].index
    model.startcons = pyo.Constraint(expr=sum(model.routes[k] for k in paths[paths.node_from==1].index)==1 )
    model.sinkcons = pyo.Constraint(expr=sum(model.routes[k] for k in paths[paths.node_to==7].index)==1 )

    model.conserve = pyo.ConstraintList()
    for node in nodes[nodes.description=='middle point'].index:
        enteringnodes = sum(model.routes[idx] for idx in paths[paths.node_to==node].index)
        leavingnodes = sum(model.routes[idx] for idx in paths[paths.node_from==node].index)
        model.conserve.add(expr = enteringnodes - leavingnodes == 0)
    
    model.obj = pyo.Objective(expr=summation(model.routes), sense=minimize)

    # opt = SolverFactory('glpk', executable='C:\\glpk-4.65\\w64\\glpsol.exe')
    opt = SolverFactory('couenne', executable='C:\\couenne\\bin\\couenne.exe')
    opt.solve(model)
    
    model.pprint()    

    for k in paths.index:
        print('Path {} : {}'.format(k, pyo.value(model.routes[k])))

run()