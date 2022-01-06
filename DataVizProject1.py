#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[11]:


line=pd.read_csv('line.csv')
wdi_scatter=pd.read_csv('wdi_scatter.csv')
wdi_new1=pd.read_csv('wdi_new1.csv')
africa_html=open("slider_map0_modified.html", 'r', encoding='utf-8')
source_code = africa_html.read() 


# In[12]:


clist=wdi_new1["Country Name"].unique()


# In[14]:


st.set_page_config(layout = "wide",initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 300px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


graph = st.sidebar.selectbox('What type of graph',['Geografical Map','Time series'])

if graph == 'Time series':
    country = st.sidebar.selectbox('Select a Country:',clist)
    st.header("**National Statistics for African states**")

    col1, col2 = st.columns(2)

    fig = px.line(wdi_new1[wdi_new1["Country Name"] == country], x="Year", y="Percentage", 
                   labels=dict(x = 'Years', y = 'Percentage of people using drinking water services'), 
                   color='Indicator Name', markers=True, range_y=[0,100],
                   title='Drinking water services for rural, urban and total population',
                template="simple_white")
    newnames = {'% of total population using drinking water services':'total population', 
                  '% of rural population using drinking water services': 'rural population',
                  '% of urban population using drinking water services': 'urban population'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                            legendgroup = newnames[t.name],
                                            hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                           )
                        )
    col1.plotly_chart(fig,use_column_width = True)

    selected=wdi_scatter[wdi_scatter["Country Name"] == country]
    fig1 = px.line(selected, 
                    x = 'Year', y = 'Value', 
                    labels=dict(x ='Years', y= 'Number of people'), color='Indicator Name', markers=True,
                    title = "Population growth vs Population with drinking services growth",
                    template="simple_white")
    
    selected2=line[line["Country Name"] == country]
    reference_line = go.Scatter(x=selected2['Year'],
                                y=selected2['Value'],
                                mode="lines", name="N. people with drinking water services if only population grow",
                                line=go.scatter.Line(color="gray"))
    
    fig1.add_trace(reference_line)
    col2.plotly_chart(fig1,use_column_width = True)
  
elif graph=='Geografical Map':
    st.sidebar.info('Remember to close the sidebar if you want to interact with the map :)')
    st.sidebar.warnings("If you can't see the slider to select year, or you see it badly, try to change broswer and use Chrome or Firefox")
    with st.container():
        st.title('Africa')
        components.html(source_code, height = 700, scrolling=False)
 

