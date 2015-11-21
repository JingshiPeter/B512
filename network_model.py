import pandas
import networkx
import pyomo.opt
import pyomo.environ as pe
import scipy
import itertools
import logging
import cplex

edge_data = {}
edge_data['From'] = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5]
edge_data['To'] = [2,3,4,5,1,3,4,5,1,2,4,5,1,2,3,5,1,2,3,4]
edge_data['Time'] = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#edge_data['Time'] = [2,2,2,1,2,2,1,2,1,2,2,1,2,2,2,2,2,2,2,2]
df_edges = pandas.DataFrame(edge_data)
print df_edges

node_data = {}
node_data['Name'] = [1,2,3,4,5]
node_data['TWS'] = [8,11,9,12,8]
node_data['TWE'] = [18,18,18,18,18]
node_data['TWS1'] = [18,18,15,18,18]
node_data['TWE1'] = [8,8,17,8,8]
df_nodes = pandas.DataFrame(node_data)
print df_nodes

#def create_graph():
g = networkx.DiGraph()
for idx,row in df_nodes.iterrows():
    g.add_node(row['Name'], A_1=row['TWS'], B_1=row['TWE'], A_2=row['TWS1'], B_2=row['TWE1'])
    
# create all edges

for node_from in g.nodes_iter(data=True):
    for node_to in g.nodes_iter(data=True):
        if node_from[0] != node_to[0]:
            print node_from[0]
            print node_to[0]
            travel_time = df_edges[(df_edges.From==(node_from[0])) & (df_edges.To==(node_to[0]))]['Time'].values[0]
            add_edge = False
            # check all four combinations, if one satisfy, add edge
            if node_from[1]['A_1'] + travel_time < node_to[1]['B_1']:
                add_edge = True
            if node_from[1]['A_1'] + travel_time < node_to[1]['B_2']:
                add_edge = True
            if node_from[1]['A_2'] + travel_time < node_to[1]['B_1']:
                add_edge = True
            if node_from[1]['A_2'] + travel_time < node_to[1]['B_2']:
                add_edge = True
            if add_edge:
                g.add_edge(node_from[0],node_to[0], cost=travel_time)
                
#add VehicleCost
for node in g.nodes_iter():
    if(node != 1):
        g.edge[1][node]['VehicleCost'] = 3000
print g.edges()      

def create_pyomo_network_lp(g,edge_cost_field='VehicleCost',node_rhs_field='b'):
    ## Create the model
    model = pe.ConcreteModel()
    ## Tell pyomo to read in dual-variable information from the solver
    model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)

    ## Associate the graph with this model
    model.g = g

    ## Create the problem data
    model.node_set = pe.Set( initialize=g.nodes() )
    model.edge_set = pe.Set( initialize=g.edges() )
    model.depot_node = pe.Set(initialize=[1])
    
    model.node_rhs = pe.Param( model.node_set, 
            initialize=lambda model, n: model.g.node[n].get(node_rhs_field,0))

    ## Only edge_cost is vehicle cost, no other cost
    model.edge_costs = pe.Param( model.edge_set, 
            initialize=lambda model, i,j: model.g.edge[i][j].get(edge_cost_field,0))


    ## Create the node variables, t_i
    model.x = pe.Var(model.node_set, domain=pe.NonNegativeReals)
    model.x_depot = pe.Var(model.depot_node, domain=pe.NonNegativeReals)
    model.x_except_depot = pe.Var(model.node_set-model.depot_node, domain=pe.NonNegativeReals)

    ## Create the variables
    model.y = pe.Var(model.edge_set, domain=pe.Binary)

    ## Create the objective
    model.OBJ = pe.Objective(expr = pe.summation(model.edge_costs, model.y)+pe.summation(model.edge_costs, model.y))

    ## Create the constraints, one for each node
    def one_in_rule(model, n):
        return ( pe.summation(model.y, index=model.g.in_edges(n)) == 1)
    def one_out_rule(model, n):
        return ( pe.summation(model.y, index=model.g.out_edges(n)) == 1)
        
    def time_A_rule(model, n):
        return ( model.x[n] >= model.g.node[n]['A_1'])
    def time_B_rule(model, n):
        return ( model.x[n] <= model.g.node[n]['B_1'])
    
    def anti_cycle_rule(model,i,j):
        if((i != 1) & (j != 1)):
            return(model.x_except_depot[i] + model.g.edge[i][j]['cost'] - model.x_except_depot[j]<= max((model.g.node[i]['B_1'] + model.g.edge[i][j]['cost'] - model.g.node[j]['A_1']),0)*(1-model.y[(i,j)]))
        else:
            return pe.Constraint.Skip
        
    model.OneIn = pe.Constraint(model.node_set-model.depot_node, rule=one_in_rule)
    model.OneOut = pe.Constraint(model.node_set-model.depot_node, rule=one_out_rule)
    model.TimeA = pe.Constraint(model.node_set-model.depot_node, rule=time_A_rule)
    model.TimeB = pe.Constraint(model.node_set-model.depot_node, rule=time_B_rule)
    model.AntiCycle = pe.Constraint(model.edge_set, rule=anti_cycle_rule)

    # Solve the model
    model.create()

    solver = pyomo.opt.SolverFactory('cplex')
    results = solver.solve(model, tee=True, keepfiles=True)

    # Check that we actually computed an optimal solution, load results
    if (results.solver.status != pyomo.opt.SolverStatus.ok):
        logging.warning('Check solver not ok?')
    if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  
        logging.warning('Check solver optimality?')

    model.load(results)

    # Print the model objective
    print 'Optimal solution value:', model.OBJ()
    
    # Load solution data back into the networkx object 
    # for e in model.edge_set:
    #     model.g.edge[e[0]][e[1]]['flow_val'] = model.y[e].value

    # for n in model.node_set:
    #     model.g.node[n]['dual_val'] = model.dual[ model.FlowBalance[n] ]

    return model
    
m = create_pyomo_network_lp(g)

#import pyomo.opt
#import pyomo.environ as pe
#model = pe.ConcreteModel()
#model.x = pe.Var([1],domain=pe.NonNegativeReals)
