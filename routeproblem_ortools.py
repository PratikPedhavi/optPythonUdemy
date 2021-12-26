import pandas as pd, numpy as np
from ortools.sat.python import cp_model

def run():
    
    file = pd.ExcelFile('.\\Inputs\\route_exercise_inputs.xlsx')
    print('Sheet Names: ', file.sheet_names)
    nodes = file.parse('nodes')
    paths = file.parse('paths')
    print(nodes)
    print(paths)
    nodes = nodes.set_index('node')
    nVars = len(paths)

    model = cp_model.CpModel()
    x = np.zeros(nVars).tolist()
    
    for p in paths.index:
        x[p] = model.NewIntVar(0,1,'x[{}]'.format([p]))
    print(x)

    objFun = sum([x[p]*paths.distance[p] for p in paths.index])
    model.Minimize(objFun)

    origin = nodes.index[nodes.description == 'origin'][0]
    destination = nodes.index[nodes.description == 'destination'][0]
    
    model.Add(sum([x[p] for p in paths[paths.node_from == origin].index]) == 1)
    model.Add(sum([x[p] for p in paths[paths.node_to == destination].index]) == 1)
    
    for node in nodes.index[nodes.description == 'middle point']:
        enteringnodes = sum(x[idx] for idx in paths[paths.node_to==node].index)
        leavingnodes = sum(x[idx] for idx in paths[paths.node_from==node].index)
        model.Add(enteringnodes == leavingnodes)

    solver = cp_model.CpSolver()  
    status = solver.Solve(model)  

    print('status: ',solver.StatusName(status))
    print('OF: ', solver.ObjectiveValue())

    paths['activated'] = 0
    for p in paths.index:
        paths.activated[p] = solver.Value(x[p])

    print(paths)


run()
