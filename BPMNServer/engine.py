import more_itertools as iter
import pm4py

import pygraphviz as pgv
import pandas as pd


from collections import defaultdict
from typing import Dict, Set
from IPython.display import Image, display

def read_file(filename, cols, event_tresh=0):
    id = cols[0]
    activity = cols[1]
    timestamp = cols[2]

    if filename.endswith(".csv"):
        df = pd.read_csv(filename, sep=';|,', usecols=cols)
    elif filename.endswith(".xes"):
        df = pm4py.convert_to_dataframe(pm4py.read_xes(filename))
        df = df.drop(
            columns=['concept:name', 'lifecycle:transition', 'case:concept:name', 'case:variant', 'case:creator'])
        df.rename(columns={'case:variant-index': id, 'Activity': activity, 'time:timestamp': timestamp}, inplace=True)
    else:
        raise Exception("File format not supported")

    df[timestamp] = pd.to_datetime(df[timestamp])

    df = (df
          .sort_values(by=[id, timestamp])
          .groupby([id])
          .agg({activity: lambda x: list(x)})
          )

    event_count = defaultdict(lambda: 0)
    for row in df[activity]:
        for event in row:
            event_count[event] = event_count[event] + 1

    filterd_event_count = defaultdict(lambda: 0)
    for event, count in event_count.items():
        if count >= event_tresh:
            filterd_event_count[event] = count

    df[activity] = df[activity].apply(lambda event_log: list(filter(lambda x: filterd_event_count[x] > 0, event_log)))
    df[activity] = df[activity].apply(lambda event_log: list(map(lambda x: x + " - " + str(event_count[x]), event_log)))
    df[activity] = df[activity].apply(lambda event_log: None if len(event_log) == 0 else event_log)
    df = df[df[activity].notna()]
    return [df, activity]


def get_direct_succesion(logs):
    direct_succesions = defaultdict(set)
    for log in logs:
        for (source, target) in iter.pairwise(log):
            direct_succesions[source].add(target)
    return direct_succesions


def get_parallel_events(direct_succession):
    parallel_events = []
    for key, succesors in list(direct_succession.items()):
        for succesor in succesors:
            if succesor in direct_succession and key in direct_succession[succesor]:
                for parallel_event in parallel_events:
                    if key in parallel_event:
                        parallel_event.add(succesor)
                parallel_event = set([key, succesor])
                if parallel_event not in parallel_events:
                    parallel_events.append(parallel_event)

    return parallel_events


def get_self_loops_and_short_loops(logs):
    self_loops = set()
    short_loops = dict()
    short_loops_via = set()
    for log in logs:
        visited = defaultdict(lambda: None)
        for ind, event in enumerate(log):
            if event not in short_loops and event not in self_loops and event not in short_loops_via:
                last_occurence = visited[event]
                if last_occurence != None:
                    if last_occurence == ind - 1:
                        self_loops.add(event)
                    elif last_occurence == ind - 2:
                        short_loops[event] = log[ind - 1]
                        short_loops_via.add(log[ind - 1])
            visited[event] = ind
    return self_loops, short_loops


def get_causality(direct_succession) -> Dict[str, Set[str]]:
    causality = defaultdict(set)
    for ev_cause, events in direct_succession.items():
        for event in events:
            if ev_cause not in direct_succession.get(event, set()):
                causality[ev_cause].add(event)
    return dict(causality)


def get_inv_causality(causality) -> Dict[str, Set[str]]:
    inv_causality = defaultdict(set)
    for key, values in causality.items():
        for value in values:
            inv_causality[value].add(key)
    return {k: v for k, v in inv_causality.items() if len(v) > 1}


class MyGraph(pgv.AGraph):
    def __init__(self, *args):
        super(MyGraph, self).__init__(strict=False, directed=True, *args)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        self.edge_attr.update(penwidth='2')
        self.multigateways = set()

    def add_event(self, name):
        super(MyGraph, self).add_node(name, shape="circle", label="")

    def add_end_event(self, name):
        super(MyGraph, self).add_node(name, shape="circle", label="", penwidth='3')

    def add_and_gateway(self, *args):
        super(MyGraph, self).add_node(*args, shape="diamond",
                                      width=".7", height=".7",
                                      fixedsize="true",
                                      fontsize="40", label="+")

    def add_xor_gateway(self, *args, **kwargs):
        super(MyGraph, self).add_node(*args, shape="diamond",
                                      width=".7", height=".7",
                                      fixedsize="true",
                                      fontsize="40", label="×")

    def add_and_split_gateway(self, source, targets, *args):
        gateway = 'ANDs ' + str(source) + '->' + str(targets)
        self.add_and_gateway(gateway, *args)
        super(MyGraph, self).add_edge(source, gateway)
        for target in targets:
            super(MyGraph, self).add_edge(gateway, target)
        return gateway

    def add_xor_split_gateway(self, source, targets, *args):
        gateway = 'XORs ' + str(source) + '->' + str(targets)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).add_edge(source, gateway)
        for target in targets:
            super(MyGraph, self).add_edge(gateway, target)
        return gateway

    def add_and_merge_gateway(self, sources, target, *args):
        gateway = 'ANDm ' + str(sources) + '->' + str(target)
        self.add_and_gateway(gateway, *args)
        super(MyGraph, self).add_edge(gateway, target)
        for source in sources:
            super(MyGraph, self).add_edge(source, gateway)
        return gateway

    def add_xor_merge_gateway(self, sources, target, *args):
        gateway = 'XORm ' + str(sources) + '->' + str(target)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).add_edge(gateway, target)
        for source in sources:
            super(MyGraph, self).add_edge(source, gateway)
        return gateway

    def connect_xor_to_and(self, sources, targets, *args):
        xor_merge_gateway = 'XORm ' + str(sources) + '->' + str(targets)
        and_split_gateway = 'ANDs ' + str(sources) + '->' + str(targets)

        multigateway = and_split_gateway + xor_merge_gateway
        if not (multigateway in self.multigateways):
            self.multigateways.add(multigateway)

            self.add_xor_gateway(xor_merge_gateway, *args)
            self.add_and_gateway(and_split_gateway, *args)
            super(MyGraph, self).add_edge(xor_merge_gateway, and_split_gateway)

            self.connect_sources_to_multigateway(sources, xor_merge_gateway)
            self.connect_gateway_to_targets(and_split_gateway, targets)

        return multigateway

    def connect_and_to_xor(self, sources, targets, *args):
        xor_split_gateway = 'XORs ' + str(sources) + '->' + str(targets)
        and_merge_gateway = 'ANDm ' + str(sources) + '->' + str(targets)

        multigateway = and_merge_gateway + xor_split_gateway
        if not (multigateway in self.multigateways):
            self.multigateways.add(multigateway)

            self.add_xor_gateway(xor_split_gateway, *args)
            self.add_and_gateway(and_merge_gateway, *args)
            super(MyGraph, self).add_edge(and_merge_gateway, xor_split_gateway)

            self.connect_sources_to_multigateway(sources, and_merge_gateway)
            self.connect_gateway_to_targets(xor_split_gateway, targets)

        return multigateway

    def connect_sources_to_multigateway(self, sources, gateway):
        for source in sources:
            super(MyGraph, self).add_edge(source, gateway)

    def connect_gateway_to_targets(self, gateway, targets):
        for target in targets:
            super(MyGraph, self).add_edge(gateway, target)


def draw_graphs(df, activity):
    logs = df[activity].to_numpy()
    G = MyGraph()

    start_set_events = set()
    end_set_events = set()

    if len(logs) == 0:
        G.draw('simple_process_model.png', prog='dot')  # empty
        return

    for log in logs:
        start_set_events.add(log[0])
        end_set_events.add(log[-1])

    direct_successions = get_direct_succesion(logs)
    causality = get_causality(direct_successions)
    inv_causality = get_inv_causality(causality)
    parallel_events = get_parallel_events(direct_successions)
    self_loops, short_loops = get_self_loops_and_short_loops(logs)
    print('self loops', self_loops)
    print('short loops', short_loops)

    # adding start event
    G.add_event("start")
    if len(start_set_events) > 1:
        for event in parallel_events:
            if set(start_set_events) <= set(event):
                G.add_and_split_gateway("start", start_set_events)
                break
        else:
            G.add_xor_split_gateway("start", start_set_events)
    else:
        G.add_edge("start", list(start_set_events)[0])

    # adding split gateways based on causality
    for event in causality:
        if len(causality[event]) > 1:
            for element in causality[event]:
                if (element in inv_causality and len(inv_causality[element]) > 1):
                    break
            else:
                if set(causality[event]) in parallel_events:
                    G.add_and_split_gateway(event, causality[event])
                else:
                    G.add_xor_split_gateway(event, causality[event])
        elif len(causality[event]) == 1:
            target = list(causality[event])[0]
            if event not in end_set_events:
                if target not in inv_causality or len(inv_causality[target]) == 1:
                    G.add_edge(event, target)

    # adding merge gateways based on inverted causality
    for event in inv_causality:
        if len(inv_causality[event]) > 1:
            targets = []
            for element in inv_causality[event]:
                if (element in causality and len(causality[element]) > 1):
                    targets = causality[element]
                    break;

            if (len(targets) == 0):
                if set(inv_causality[event]) in parallel_events:
                    G.add_and_merge_gateway(inv_causality[event], event)
                else:
                    G.add_xor_merge_gateway(inv_causality[event], event)
            else:
                if set(inv_causality[event]) in parallel_events:
                    G.connect_and_to_xor(inv_causality[event], targets)
                else:
                    G.connect_xor_to_and(inv_causality[event], targets)

    G.add_end_event("end")
    final_end_events = set()
    final_end_gateways = set()
    for event in end_set_events:
        if event in causality:
            final_end_gateways.add(G.add_xor_split_gateway(event, causality[event]))
        else:
            final_end_events.add(event)

    end_objects = set()
    for event in final_end_events:
        end_objects.add(event)
    for event in final_end_gateways:
        end_objects.add(event)

    if len(end_objects) > 1:
        for event in parallel_events:
            if set(end_set_events) <= set(event):
                G.add_and_merge_gateway(end_objects, "end")
                break
        else:
            G.add_xor_merge_gateway(end_objects, "end")
    else:
        G.add_edge(list(end_objects)[0], "end")

    G.draw('simple_process_model.png', prog='dot')
    display(Image('simple_process_model.png'))


def draw_and_save(filename, cols, tsh):
    if cols == None or len(cols) != 3:
        # fallback to default
        cols = ["Case ID", "Activity", "Start Timestamp"]
    draw_graphs(*read_file(filename, cols, event_tresh=tsh))
