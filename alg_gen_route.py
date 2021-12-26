import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga
from pdb import set_trace

def f(x):
    pen = 0

    origin = int(nodes.node[nodes.description == 'origin'])
    destination = int(nodes.node[nodes.description == 'destination'])

    if sum([x[p] for p in paths.index[paths.node_from==origin]]) != 1:
        pen += 1000000 * np.abs(sum([x[p] for p in paths.index[paths.node_from==origin]]) - 1)

    if sum([x[p] for p in paths.index[paths.node_to==destination]]) != 1:
        pen += 1000000 * np.abs(sum([x[p] for p in paths.index[paths.node_to==destination]]) - 1)

    for node in nodes.node[nodes.description == 'middle point']:
        incoming = sum([x[p] for p in paths.index[paths.node_to==node]])
        outgoing = sum([x[p] for p in paths.index[paths.node_from==node]])
        if incoming != outgoing:
            pen += 1000000 * np.abs(incoming - outgoing)

    obj = sum([x[p]*paths.distance.iloc[p] for p in paths.index])
    return obj + pen

file = pd.ExcelFile(r'Inputs\route_inputs.xlsx')
print('Sheet Names: ', file.sheet_names)
nodes = file.parse('nodes')
paths = file.parse('paths')
print(nodes)
print(paths)
nVars = len(paths)

# varbound = np.array([[0,1] for _ in range(nVars)])
# vartype = np.array(['int' for _ in range(nVars)])
varbound = np.array([[0,1]]*nVars)
vartype = np.array([['int']]*nVars)

algo_param = {'max_num_iteration':500,
            'population_size':100,
            'mutation_probability':0.30,
            'elit_ratio':0.10,
            'crossover_probability':0.50,
            'parents_portion':0.30,
            'crossover_type':'uniform',
            'max_iteration_without_improv':100}

model = ga(function=f, dimension=nVars,
            variable_type_mixed=vartype,
            variable_boundaries=varbound,
            algorithm_parameters=algo_param)

model.run()

x = model.best_variable
obj = model.best_function
paths['activated'] = 0
for p in paths.index:
    paths.activated[p] = x[p]

print('Selected Routes ')
print(paths[paths['activated']==1])
