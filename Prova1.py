#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[2]:


line=pd.read_csv('line.csv')
wdi_scatter=pd.read_csv('wdi_scatter.csv')
wdi_new1=pd.read_csv('population_percentage.csv')
africa_html=open("slider_maps.html", 'r', encoding='utf-8')
source_code = africa_html.read() 


wdi_scatter['Value']=round(wdi_scatter['Value'],0)

# In[12]:


clist=wdi_new1["Country Name"].unique()


# In[1]:


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
    st.title("National Statistics for %s" % (country))
    st.write('''In this section you can explore in more detail the change over time for a specific country, only states with information available for each year since 2000 are 
              selectable.''')

    col1, col2 = st.columns(2)

    fig = px.line(wdi_new1[wdi_new1["Country Name"] == country], x="Year", y="Percentage (%)", 
                   labels={"Indicator Name":"Indicator", "Year":"Year", "Percentage (%)":"Percentage (%)"}, 
                   color='Indicator Name', markers=True, range_y=[0,100],
                   title='<b>Population(%) with access to basic water services</b>',
                   template="seaborn", 
                   color_discrete_map={ '% of urban population using drinking water services': "blue", 
                                        '% of total population using drinking water services': "orange",
                                        '% of rural population using drinking water services': "green"},
                   category_orders={"Indicator Name": ['% of urban population using drinking water services',
                                                       '% of total population using drinking water services',
                                                       '% of rural population using drinking water services']})
    
    newnames = {'% of urban population using drinking water services': '% of urban population',
                '% of total population using drinking water services':'% of total population', 
                '% of rural population using drinking water services': '% of rural population'}
    
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                          legendgroup = newnames[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                           )
                        )
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(legend_title_text='')
    fig.update_xaxes(nticks=20, autorange=True)
    col2.plotly_chart(fig,use_column_width = True)

    selected=wdi_scatter[wdi_scatter["Country Name"] == country]
    
    fig1 = px.line(selected, 
                   x = 'Year', y = 'Value', 
                   labels={"Indicator Name":"Indicator", "Year":"Year", "Value":"Population"},
                   color='Indicator Name', markers=True,
                   title = "<b>Total and with access to basic water services population growth</b>",
                   template="seaborn", 
                   color_discrete_map={ "Total population": "red", "Number of people using drinking water services": "purple" },
                   category_orders={"Indicator Name": ['Total population',
                                                       'Number of people using drinking water services']})
    
    newnames = {'Total population': 'Total population',
                'Number of people using drinking water services':'PUW (People using basic water services)'}
    
    fig1.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                          legendgroup = newnames[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                           )
                        )
    
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig1.update_layout(legend_title_text='')
    
    selected2=line[line["Country Name"] == country]
    reference_line = go.Scatter(x=selected2['Year'],
                                y=selected2['Value'],
                                fill=None, hovertext="",
                                mode="lines", name=r'PUW if no percentage change in PUW since 2000',
                                line=go.scatter.Line(color="grey", dash='dot'))
    
    fig1.add_trace(reference_line)
    fig1.update_yaxes(rangemode="tozero")
    fig1.update_xaxes(nticks=20)
    col1.plotly_chart(fig1,use_column_width = False) 

elif graph=='Geografical Map':
    st.sidebar.info('Remember to close the sidebar to fully interact with the map :)')
    with st.container():
        st.title(r'Access to water in Africa is not yet to be taken for granted')
        st.write('''On 28 July 2010 the United Nations General Assembly recognized the human right to water as fundamental also for the realization of other human rights. 
                    Despite this declaration in 2020 the level of availability and access to basic drinking water services was particularly low in many countries of the African continent.
                    Such services are those including water from an improved source, so that provided collection time is not more than 30 minutes for a round trip.
                    On the map below you can have a general wiev in how the situation changed in different states of the continent since 2000 both for the percentual of people 
                    with access to basic drinking services and for the inequalities between urban and rural population. More insights about statistics of the single states can be found in 
                    the section relative to the time series (click on the arrow at the top left to access such section).''')
        components.html(source_code, height = 700, scrolling=False)
        st.markdown('<a href="https://www.flaticon.com/free-icons/information" title="information icons">Information icons created by Freepik - Flaticon</a>',unsafe_allow_html=True)

