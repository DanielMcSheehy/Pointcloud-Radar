import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
import time
import psutil
import math
import plotly.graph_objects as go
import cv2
import plotly.express as px
import time

def format(pid,cpu_percent, name, children=[]):
    return {"pid": str(pid), "cpu": cpu_percent, "name": name, "children": children}

def handle_children(list): 
    return [format(p.pid, p.cpu_percent(), p.name()) for p in list if p.status() != psutil.STATUS_ZOMBIE]

def handle_process(p):
    return format(p.pid, p.info["cpu_percent"], p.info['name'] , handle_children(p.children(recursive=False)))
    
def get_processes(): 
        thing = [(str(p.pid), handle_process(p)) for p in psutil.process_iter(["name", "cpu_percent"]) if (p.info["cpu_percent"] or 0) > 0]
        return {k:v for (k, v) in thing}
    
def gen_hierachy(): 
    st.title('Processes')
    processes = get_processes()
    parents = [""]
    labels = ["root"]
    values = [1]

    def free(list, key):
        return key not in list

    for (k,v) in processes.items(): 
        key = k + v["name"]
        if free(labels, key):
            labels.append(k + v["name"])
            parents.append("root")
            values.append(v["cpu"])
            
            for child in v["children"]:
                child_key = child["pid"] + child["name"]
                if free(labels, child_key):
                    parents.append(k + v["name"])
                    labels.append(child_key)
                    values.append(child["cpu"] + 0.1)
    return {"parents": parents, "labels": labels, "values": values}

def start_sunburst_and_ice_plots():
    result = gen_hierachy()
    fig =go.Figure(go.Sunburst(
        labels=result['labels'],
        parents=result["parents"],
        values=result["values"],
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    st.plotly_chart(fig, use_container_width=True)

    icicle =px.icicle(
        names=result['labels'],
        parents=result["parents"],
        values=result["values"],
    )
    icicle.update_traces(root_color="lightgrey")
    icicle.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(icicle, use_container_width=True)
