import streamlit as st

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Malaysia's Electricity Generation (1955-2018)")

#sidebar
#sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#year slider
year = st.sidebar.slider('YEAR',1955,2018)
st.sidebar.text(f'Year Selected: {year}')



#read dataset
data = pd.read_excel('elektrik.xlsx', sheet_name='format')
data.dropna(subset=['generated'],inplace=True)
data.drop(data.loc[data['generated']==0].index, inplace=True)
data['generated'] = data['generated'].apply(lambda x:round(x,2))



#plot 1st graph
total_gen = data.groupby('year')['generated'].sum()

status_1 = st.radio('Show: ', ('Total Electricity Generated','Animation'))
if status_1 == 'Total Electricity Generated':
    fig = plt.figure(figsize=(10,5))
    filter_year = plt.plot(total_gen.iloc[:year-1954])
    plt.title(f'Total Electricity Generated by Year (1955-{year})')
    plt.xlim(1950,2020)
    plt.xlabel('Year')
    plt.ylabel('Electricity Generated (KWH)')
    st.write(fig)
else:
    st.text('COMING SOON')
    


#plot 2nd graph
year_type = pd.DataFrame({'steam':data[data['type']=='steam'].groupby('year')['generated'].sum(),
                          'diesel':data[data['type']=='diesel'].groupby('year')['generated'].sum(),
                          'hydro':data[data['type']=='hydro'].groupby('year')['generated'].sum(),
                          'gas':data[data['type']=='gas'].groupby('year')['generated'].sum(),
                          'coal':data[data['type']=='coal'].groupby('year')['generated'].sum(),
                          'others':data[data['type']=='others'].groupby('year')['generated'].sum()})
                          
status_2 = st.radio('Show: ', ('Types of Electricity Generated','Animation'))
if status_2 == 'Types of Electricity Generated':
    fig = plt.figure(figsize=(10,5))
    filter_year = plt.plot(year_type.iloc[:year-1954])
    plt.title(f'Types of Electricity Generated by Year (1955-{year})')
    plt.legend(['steam','diesel','hydro','gas','coal','others'])
    plt.xlabel('Year')
    plt.ylabel('Electricity Generated (KWH)')
    st.write(fig)
else:
    st.text('COMING SOON')



#selection box for type
elec_type = ['steam','diesel','hydro','gas','coal','others']
type = st.selectbox('Stations:', elec_type) 

#plot 2.1 graph
fig = plt.figure(figsize=(10,5))
filter_year = plt.plot(year_type[type].iloc[:year-1954])
plt.title(f'Electricity Generated from {type.capitalize()} Stations by Year (1955-{year})')
plt.xlim(1950,2020)
plt.xlabel('Year')
plt.ylabel('Electricity Generated (KWH)')
st.write(fig)



#plot 3th graph
status_3 = st.radio('Show: ', ('Bar Chart','Animation'))

if status_3 == 'Bar Chart':
    fig = plt.figure(figsize=(10,5))
    plt.bar(data[data['year']==year].groupby('type')['generated'].sum().index,
            data[data['year']==year].groupby('type')['generated'].sum())
    plt.title(f'Total Electricity Generated in {year}')
    plt.xlabel('Types of Stations')
    plt.ylabel('Electricity Generated (KWH)')
    st.write(fig)   
else:
    st.text('COMING SOON')



#plot 4th graph
def diff(type, year):
    if year > 1955:
        if year_type.diff()[type][year] > year_type.diff()[type][year-1]:
            st.success('Increase')
        elif year_type.diff()[type][year] < year_type.diff()[type][year-1]:
            st.error('Decrease')
        else:
            st.text('-')
    else:
        st.text('-')

st.sidebar.header('Generated Difference (KWH)')        
row1_1, row1_2, row1_3 = st.sidebar.beta_columns((1,1,1))
with row1_1:
    st.subheader('Steam Stations')
    st.write('{0:.2f}'.format(year_type.diff()['steam'][year]))
    diff('steam',year)
    
with row1_2:
    st.subheader('Diesel Stations')
    st.write('{0:.2f}'.format(year_type.diff()['diesel'][year]))
    diff('diesel',year)
    
with row1_3:
    st.subheader('Hydro Stations')
    st.write('{0:.2f}'.format(year_type.diff()['hydro'][year]))
    diff('hydro',year)

row2_1, row2_2, row2_3 = st.sidebar.beta_columns((1,1,1))
with row2_1:
    st.subheader('Gas Stations')
    st.write('{0:.2f}'.format(year_type.diff()['gas'][year]))
    diff('gas',year)
    
with row2_2:
    st.subheader('Coal Stations')
    st.write('{0:.2f}'.format(year_type.diff()['coal'][year]))
    diff('coal',year)
    
with row2_3:
    st.subheader('Others')
    st.write('{0:.2f}'.format(year_type.diff()['others'][year]))
    diff('others',year)



#plot pie chart    
fig = plt.figure(figsize=(10,5))

plt.pie(data[data['year']==year].groupby('installations')['generated'].sum(), 
        explode = (0.5,0),
        autopct = '%1.0f%%',
        labels = ['Private','Public'])

plt.title(f'Total Electricity Generated based on Installations Type in {year}')
plt.legend(['Private','Public'])
st.sidebar.write(fig)

