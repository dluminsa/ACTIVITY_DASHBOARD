import pandas as pd 
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
     page_title= 'ACTIVITY TRACKER'
)
cola,colb,colc = st.columns([1,2,1])
cola.write('')
colb.markdown("<h4><b>ACTIVITIES DASHBOARD</b></h4>", unsafe_allow_html=True)
colc.write('')
current_time = time.localtime()
k = time.strftime("%V", current_time)
cola,colb,colc = st.columns([1,2,1])
cola.write(f'**CURRENT WEEK IS: {k}**')
conn = st.connection('gsheets', type=GSheetsConnection)

dfb = conn.read(worksheet='DONE', usecols=list(range(11)), ttl=5)
dfb = dfb.dropna(how='all')

dfb= dfb[['CLUSTER','DISTRICT', 'AREA','ACTIVITY', 'DONE', 'WEEK','FACILITY']]
file = r'C:\Users\Desire Lumisa\Desktop\PAPER\PLANNED.csv'
dfa = pd.read_csv(file)


dfa= dfa[['DISTRICT', 'AREA','ACTIVITY', 'PLANNED']]

dfb['WEEK'] = dfb['WEEK'].astype(int)
dfb['DISTRICT'] = dfb['DISTRICT'].astype(str)
dfb['AREA'] = dfb['AREA'].astype(str)
dfb['ACTIVITY'] = dfb['ACTIVITY'].astype(str)
dfb['DONE'] = dfb['DONE'].astype(int)

dfa['DISTRICT'] = dfa['DISTRICT'].astype(str)
dfa['AREA'] = dfa['AREA'].astype(str)
dfa['ACTIVITY'] = dfa['ACTIVITY'].astype(str)
dfa['PLANNED'] = dfa['PLANNED'].astype(int)


st.sidebar.subheader('Filter from here ')
district = st.sidebar.multiselect('Pick a district', dfa['DISTRICT'].unique())

if not district:
    dfa2 = dfa.copy()
    dfb2 = dfb.copy()
else:
    dfa2 = dfa[dfa['DISTRICT'].isin(district)]
    dfb2 = dfb[dfb['DISTRICT'].isin(district)]

#create for district
area = st.sidebar.multiselect('Choose a thematic area', dfa2['AREA'].unique())
if not area:
    dfa3 = dfa2.copy()
    dfb3 = dfb2.copy()
else:
    dfa3 = dfa2[dfa2['AREA'].isin(area)]
    dfb3 = dfb2[dfb2['AREA'].isin(area)]
 
#for facility
activity = st.sidebar.multiselect('Choose an activity', dfa3['ACTIVITY'].unique())

#Filter Week, District, Facility
if not district and not area and not activity:
    filtered_dfa = dfa
    filtered_dfb = dfb
elif not area and not activity:
    filtered_dfa = dfa[dfa['DISTRICT'].isin(district)]
    filtered_dfb = dfb[dfb['DISTRICT'].isin(district)]
elif not district and not activity:
    filtered_dfa = dfa[dfa['AREA'].isin(area)]
    filtered_dfb = dfb[dfb['AREA'].isin(area)]
elif area and activity:
    filtered_dfa = dfa3[dfa['AREA'].isin(area)& dfa3['ACTIVITY'].isin(activity)]
    filtered_dfb = dfb3[dfb['AREA'].isin(area)& dfb3['ACTIVITY'].isin(activity)]
elif district and activity:
    filtered_dfa = dfa3[dfa['DISTRICT'].isin(district)& dfa3['ACTIVITY'].isin(activity)]
    filtered_dfb = dfb3[dfb['DISTRICT'].isin(district)& dfb3['ACTIVITY'].isin(activity)]
elif district and area:
    filtered_dfa = dfa3[dfa['DISTRICT'].isin(district)& dfa3['AREA'].isin(area)]
    filtered_dfb = dfb3[dfb['DISTRICT'].isin(district)& dfb3['AREA'].isin(area)]
elif activity:
    filtered_dfa = dfa3[dfa3['ACTIVITY'].isin(activity)]
    filtered_dfb = dfb3[dfb3['ACTIVITY'].isin(activity)]
else:
    filtered_dfa = dfa3[dfa3['DISTRICT'].isin(district) & dfa3['AREA'].isin(area)&dfa3['ACTIVITY'].isin(activity)]
    filtered_dfb = dfb3[dfb3['DISTRICT'].isin(district) & dfb3['AREA'].isin(area)&dfb3['ACTIVITY'].isin(activity)]
#################################################################################################
cols,cold = st.columns(2)
dist = filtered_dfb['DISTRICT']. unique()
if not district:
    pass
elif len(dist) == 0:
    cols.write(f'**No data for this district**')
else:
    cols.write(f'**You are viewing data for: {dist}**')

ar = filtered_dfb['AREA']. unique()
if len(ar) == 0:
    cold.write(f'**No data for the thematic area(s) chosen**')
else:
    cold.write(f'**The data set is filtered by: {ar} thematic area(s)**')

act = filtered_dfb['ACTIVITY']. unique()

if not activity:
    st.write(f'**No specific activity has been chosen**')
elif len(act) == 0:
    st.write(f'**No data for the the activity chosen**')
else:
    st.write(f'**ACTIVITIES INCLUDED ARE: {act}**')

plan = filtered_dfa['PLANNED'].sum()
conducted = filtered_dfb['DONE'].sum()
notdone = plan - conducted
perc = round((conducted/plan)*100)

if conducted>plan:
    st.warning(f"SOMETHING IS WRONG, IT SEEMS ACTIVITIES DONE ARE MORE THAN THOSE THAT WERE PLANNED FOR!!")

col1,col2,col3,col4 = st.columns(4, gap='large')

with col1:
    st.metric(label='**PLANNED**', value=f'{plan:,.0f}')
with col2:
    st.metric(label='**CONDUCTED**', value=f'{conducted:,.0f}')
with col3:
    st.metric(label='**PERCENTAGE**', value=f'{perc:,.0f}')
with col4:
    st.metric(label='**NOT DONE**', value=f'{notdone:,.0f}')

#######################################################################################################
#PIE CHART
#st.divider()
col1, col2,col3 = st.columns([1,4,1])
labels = ['DONE', 'NOTDONE']
# Values
values = [conducted, notdone]
colors = ['blue', 'red']
# Creating the pie chart with specified colors and hole
fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+value', 
                             insidetextorientation='radial', marker=dict(colors=colors), hole=0.4)])

# Updating the layout for better readability
fig.update_traces(textposition='inside', textfont_size=20)
fig.update_layout(title_text='DONE vs NOTDONE', title_x=0.3)

col1, col2,col3 = st.columns([1,4,1])
with col2:
     st.plotly_chart(fig, use_container_width=True)
#############################################################################################
#LINE GRAPH
st.divider()

grouped = filtered_dfb.groupby('WEEK').sum(numeric_only=True).reset_index()
fig2 = px.line(grouped, x='WEEK', y='DONE', title='WEEKLY TRENDS',
               markers=True)

fig2.update_layout(xaxis_title='WEEK', yaxis_title='TOTAL DONE',
                    width=800,  # Set the width of the plot
                     height=400,  # Set the height of the plot
                     xaxis=dict(showline=True, linewidth=1, linecolor='black',tickmode='linear',tick0=25,dtick=1,),  # Show x-axis line
                     yaxis=dict(showline=True, linewidth=1, linecolor='black'))  # Show y-axis line)

st.plotly_chart(fig2, use_container_width=True)

filtered_dfc= filtered_dfb[['CLUSTER','DISTRICT','FACILITY' ,'AREA','ACTIVITY', 'DONE', 'WEEK']]
with st.expander(f'**CLICK HERE TO SEE FULL DATA SET**'):
    st.dataframe(filtered_dfc.reset_index(drop=True))
    csv_data = filtered_dfc.to_csv(index=False)
    st.download_button(
                        label=" DOWNLOAD THIS DATA SET",
                        data=csv_data,
                        file_name="ACTIVITIES.csv",
                        mime="text/csv")
    