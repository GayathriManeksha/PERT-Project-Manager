from asyncio import tasks
import pandas as pd
import datetime

import matplotlib.pyplot as plt
import networkx as nx
from criticalpath import Node
import plotly.express as px
from IPython.display import Image , display
from datetime import date

# tasks = [("A", {"Duration": 3}), 
#          ("B", {"Duration": 5}), 
#          ("C", {"Duration": 2}), 
#          ("D", {"Duration": 3}), 
#          ("E", {"Duration": 5})]
# tasks=[]
def add_nodes(tasks,key,value):
    item=(key,{"Duration":value})
    # item[key]={"Duration":value}
    tasks.append(item)

# add_nodes("A",3)
# add_nodes("B",5)
# add_nodes("C",2)
# add_nodes("D",3)
# add_nodes("E",5)
# set up the dependencies along all paths:
# dependencies = [("A", "C"), 
#                 ("B", "C"), 
#                 ("A", "D"),
#                 ("C", "E"), 
#                 ("D", "E")]

# dependencies=[]
def add_edges(dependencies,edge1,edge2):
    item=(edge1,edge2)
    dependencies.append(item)

# add_edges("A","C")
# add_edges("B","C")
# add_edges("A","D")
# add_edges("C","E")
# add_edges("D","E")

def critical_path(dependencies,tasks):
        # initialize (directed) graph
    G = nx.DiGraph() 

    # add tasks and dependencies (edges)
    G.add_nodes_from(tasks)
    G.add_edges_from(dependencies)

    # set up the (arbitrary) positions of the tasks (nodes):
    pos_nodes = {"A": (1, 3), 
                "B": (1, 1), 
                "C": (2, 2), 
                "D": (3, 3), 
                "E": (4, 2)}

    # draw the nodes
    nx.draw(G, with_labels=True, pos=pos_nodes, node_color='lightblue', arrowsize=20)

    # set up the (arbitrary) positions of the durations labels (attributes):
    pos_attrs = {node:(coord[0], coord[1] + 0.2) for node, coord in pos_nodes.items()}
    attrs = nx.get_node_attributes(G, 'Duration')

    # draw (write) the node attributes (duration)
    nx.draw_networkx_labels(G, pos=pos_attrs, labels=attrs)


    # set a little margin (padding) for the graph so the labels are not cut off
    plt.margins(0.1)


    # initialize a "project":
    proj = Node('Project')

    # load the tasks and their durations:
    for t in tasks:
        proj.add(Node(t[0], duration=t[1]["Duration"]))

    # load the dependencies (or sequence):
    for d in dependencies:
        proj.link(d[0],d[1])

    # update the "project":
    proj.update_all()

    # proj.get_critical_path() will return a list of nodes
    # however, we want to store them as strings so that they can be easily used for visualization later
    crit_path = [str(n) for n in proj.get_critical_path()]

    # get the current duration of the project
    proj_duration = proj.duration

    print(f"The current critical path is: {crit_path}")
    print(">"*50)
    print(f"The current project duration is: {proj_duration} days")




#GANTT-CHART
def gc(dependencies,crit_path):
    proj_startdate = date.today()

    proj_schedule = pd.DataFrame([dict(Task = key, 
                                    Start = datetime.date.today(), 
                                    Finish = datetime.date.today() + datetime.timedelta(val['Duration']), 
                                    Status = 'NA')
                                for key, val in dict(tasks).items()])

    for key, val in dict(tasks).items():
        dep = [d for d in dependencies if d[1] == key]
        prev_tasks = [t[0] for t in dep]
        if prev_tasks:
            prev_finish = proj_schedule[proj_schedule.Task.isin(prev_tasks)]['Finish'].max()
            proj_schedule.loc[proj_schedule.Task == key, 'Start'] = prev_finish
            proj_schedule.loc[proj_schedule.Task == key, 'Finish'] = prev_finish + datetime.timedelta(val['Duration'])
            
    proj_schedule.loc[proj_schedule.Task.isin(crit_path), 'Status'] = 'Critical Path'
            
    display(proj_schedule)

# fig = px.timeline(proj_schedule, x_start="Start", x_end="Finish", y="Task", color="Status")
# fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
#Image(fig.to_image(format="png"))