#!/usr/bin/env python
# coding: utf-8

# In[122]:


import numpy as np
import pandas as pd
wdi=pd.read_csv('Desktop\dataviz\WDIData.csv')
country=pd.read_csv('Desktop\dataviz\WDICountry.csv')


# In[123]:


sub_saharan_africa=country[country['Region']=='Sub-Saharan Africa']['Short Name']
wdi_sub_saharan_africa=wdi[wdi['Country Name'].isin(sub_saharan_africa)]
i1='People using at least basic drinking water services (% of population)'
i2='People using at least basic drinking water services, rural (% of rural population)'
i3='People using at least basic drinking water services, urban (% of urban population)'
i=[i1,i2,i3]
wdi_sub_saharan_africa_water=wdi_sub_saharan_africa[wdi_sub_saharan_africa['Indicator Name'].isin(i)]
wdi_new=wdi_sub_saharan_africa_water


# In[124]:


i4='Population, total'
j=[i1,i4]
wdi_sub_saharan_africa_scatter=wdi_sub_saharan_africa[wdi_sub_saharan_africa['Indicator Name'].isin(j)]


# In[125]:


year_of_interest=[]
for year in wdi.columns[44:65]:
    wdi_new=wdi_new[wdi_new[year].isnull()==False]
    year_of_interest.append(year)


# In[126]:


wdi_new=wdi_new[["Country Name","Country Code","Indicator Name","2000","2001",'2002','2003','2004','2005','2006','2007','2008','2009','2010',
                      '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']]


# In[127]:


wdi_scatter=wdi_sub_saharan_africa_scatter[["Country Name","Country Code","Indicator Name","2000","2001",'2002','2003','2004','2005','2006','2007','2008','2009','2010',
                      '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']]


# In[128]:


wdi_scatter=wdi_scatter.melt(id_vars=["Country Name", "Country Code","Indicator Name"], 
        var_name="Year", 
        value_name="Value")


# In[129]:


import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[130]:


clist=wdi_new["Country Name"].unique()


# In[131]:


wdi_new1=wdi_new.melt(id_vars=["Country Name", "Country Code","Indicator Name"], 
        var_name="Year", 
        value_name="Percentage")


# In[132]:


line=wdi_scatter


# In[133]:


index=pd.Index(range(0,1805,2))
pop=wdi_scatter[wdi_scatter['Indicator Name']==i4]
pop=pop.set_index(index)
perc=wdi_scatter[wdi_scatter['Indicator Name']==i1]
perc_new=perc[perc['Year']=='2000']
perc_new = pd.concat([perc_new]*21, ignore_index=True)
perc_new=perc_new.set_index(index)
line.loc[index, 'Value']=(perc_new['Value'])*((pop['Value'])/100)
line=line[line["Indicator Name"]==i1]


# In[137]:


wdi_scatter.loc[index, 'Value'] = ((perc['Value'])/100)*(pop['Value'])


# In[138]:


wdi_new1["Indicator Name"]=wdi_new1["Indicator Name"].replace({"People using at least basic drinking water services (% of population)": "% of total population using drinking water services",
                                    "People using at least basic drinking water services, rural (% of rural population)": "% of rural population using drinking water services",
                                   'People using at least basic drinking water services, urban (% of urban population)':'% of urban population using drinking water services'})


# In[139]:


wdi_scatter["Indicator Name"]=wdi_scatter["Indicator Name"].replace({"People using at least basic drinking water services (% of population)": "Number of people using drinking water services",
                                                                    'Population, total': 'Total population'})


# In[140]:


line["Indicator Name"]=line["Indicator Name"].replace({"People using at least basic drinking water services (% of population)": "Number of people using drinking water services if only population grows"})


# In[144]:


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

