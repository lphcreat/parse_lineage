from d3graph import d3graph, vec2adjmat
import re
import random

source_table_regex = re.compile(r"(?:from|join)\s+(\S*)(?:\s+|;)")
target_table_regex = re.compile(r"insert\s+(?:into|overwrite)\s+table\s+(\S*)\s+")

def get_randColor(seed):
    r = random.randint(0, 200)
    g = random.randint(0, 150)
    b = random.randint(0, 200)
    return '#%02x%02x%02x' % (r,g,b)

def get_edges(dir,filter_tb):
    file_list=[]
    if isinstance(dir,list):
        file_list=dir
    elif isinstance(dir,str):
        if dir.endswith('/'):
            import os
            file_list=map(lambda f:dir+f,filter(lambda x:x.endswith(('.conf','.sql')),os.listdir(dir)))
        elif dir.endswith(('.conf','.sql')):
            file_list=[dir]
        else:
            raise FileNotFoundError("path not found please end with /|.sql|.conf")
    else:
        raise FileNotFoundError("you can set dir with file list or path")
    
    sources=[]
    targets=[]
    for file in file_list:
        with open(file,'r', encoding='utf-8') as f:
            conf_str=f.read().replace('"',' ').replace(')',' )').lower()
            source=list(filter(lambda x:'.' in x,re.findall(source_table_regex,conf_str)))
            target=re.findall(target_table_regex,conf_str)[:1]*len(source)
        sources.extend(source)
        targets.extend(target)
    if filter_tb:
        import pandas as pd
        df_temp=pd.DataFrame({'sour':sources,'targ':targets})
        df_temp=df_temp[(df_temp['sour']==filter_tb)|(df_temp['targ']==filter_tb)]
        adjmat = vec2adjmat(df_temp.sour, df_temp.targ)
    else:
        adjmat = vec2adjmat(sources, targets)
    return adjmat

def draw_graph(dir,filter_tb=False):
    adjmat=get_edges(dir,filter_tb)
    d3 = d3graph(support='li')
    d3.graph(adjmat)
    nodes=d3.node_properties.keys()
    d3.set_edge_properties(directed=True,minmax=[1, 20], scaler='minmax')
    unique_dbs=set((node.split('.')[0] for node in nodes))
    color_dict=dict(zip(unique_dbs,map(get_randColor,unique_dbs)))
    colors=[color_dict.get(node.split('.')[0]) for node in nodes]
    d3.set_node_properties(color=colors)
    d3.show()


if __name__ == '__main__':
    import sys
    base_dir=sys.argv[1]
    draw_graph(base_dir)
    if len(sys.argv)==3:
        filter_tb = sys.argv[2]
        draw_graph(base_dir,filter_tb)
    