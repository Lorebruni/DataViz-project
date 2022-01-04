#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[2]:


line=pd.read_csv('line.csv')
wdi_scatter=pd.read_csv('wdi_scatter.csv')
wdi_new1=pd.read_csv('wdi_new1.csv')


# In[6]:


clist=wdi_new1["Country Name"].unique()


# In[7]:


st.set_page_config(layout = "wide")
country = st.sidebar.selectbox('Select a Country:',clist)
st.header("**National Statistics for African states**")

col1, col2 = st.columns(2)

fig = px.line(wdi_new1[wdi_new1["Country Name"] == country], x="Year", y="Percentage", 
             labels=dict(x = 'Years', y = 'Percentage of people using drinking water services'), 
             color='Indicator Name', markers=True, range_y=[0,100],
             title='Drinking water services for rural, urban and total population',
             template="simple_white")
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
                            mode="lines", name="If only population change",
                            line=go.scatter.Line(color="gray"))
fig1.add_trace(reference_line)

col2.plotly_chart(fig1,use_column_width = True)


# In[ ]:




