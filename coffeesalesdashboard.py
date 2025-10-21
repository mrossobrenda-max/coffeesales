import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit as st
#load dataset
df = pd.read_csv("data/Coffe_sales.csv")
#streamlit
st.title("☕Coffee Sales Dashboard")
st.subheader("Analytical Summary")
#visuals
corr = df[['hour_of_day','money','Weekdaysort','Monthsort']].corr()
heat_fig = px.imshow(corr, text_auto='.3f',color_continuous_scale='Greens',aspect='auto',title='Correlation between time and coffee sales')
#resize the visual
heat_fig.update_layout(
    width=600,
    height=400,
)
heat_map = px.imshow(corr, text_auto='.3f',color_continuous_scale='Greens',aspect='auto',title='Correlation between time and coffee sales')
#resize the visual
heat_map.update_layout(
    width=600,
    height=400,
)
st.plotly_chart(heat_fig, use_container_width=True) #selectbox
st.plotly_chart(heat_map, use_container_width=True)
#regplot to show correlation btn sales and hourofday
x = df['money']
y  = df['hour_of_day']
#regplot to show correlation btn sales and hourofday
coeffs= np.polyfit(x,y,1)
regline = np.poly1d(coeffs)
x_range=np.linspace(x.min(),x.max(),20)
ypred=regline(x_range)
#create the scatter/regplot
reg_fig = go.Figure()
reg_fig.add_trace(go.Scatter(x=x,y=ypred, mode='markers', name='Coffee Sales',marker=dict(color='green'))) #scatter datapoints
reg_fig.add_trace(go.Scatter(x=x_range,y=ypred, mode='lines', name='Hours of Day',line=dict(color='green'))) #regression line
reg_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    title='How hour of the day affects the Coffee sales',
    xaxis_title='Sales',
    yaxis_title='Hour of Day',
    colorway=['#ff0000','#00ff00','#0000ff'],
)
#regplot to show correlation btn sales and hourofday
coeffs= np.polyfit(x,y,1)
regline = np.poly1d(coeffs)
x_range=np.linspace(x.min(),x.max(),20)
ypred=regline(x_range)
#create the scatter/regplot
reg_plot = go.Figure()
reg_plot.add_trace(go.Scatter(x=x,y=ypred, mode='markers', name='Coffee Sales',marker=dict(color='green'))) #scatter datapoints
reg_plot.add_trace(go.Scatter(x=x_range,y=ypred, mode='lines', name='Hours of Day',line=dict(color='green'))) #regression line
reg_plot.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    title='How hour of the day affects the Coffee sales',
    xaxis_title='Sales',
    yaxis_title='Hour of Day',
    colorway=['#ff0000','#00ff00','#0000ff'],
)
st.plotly_chart(reg_fig, use_container_width=True) #selectbox
st.plotly_chart(reg_plot, use_container_width=True) #streamlit
#lets understand the coffeetypes sales using a countplot
coffeecount = df['coffee_name'].value_counts().reset_index()
coffeecount.columns = ['Coffee_types','Count']
count_fig = px.bar(coffeecount, x='Coffee_types', y='Count',orientation='v',title='Coffee type sales distribution',color='Count',color_continuous_scale='Greens')
count_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
coffeecount = df['coffee_name'].value_counts().reset_index()
coffeecount.columns = ['Coffee_types','Count']
count_plot = px.bar(coffeecount, x='Coffee_types', y='Count',orientation='v',title='Coffee type sales distribution',color='Count',color_continuous_scale='Greens')
count_plot.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
st.plotly_chart(count_fig, use_container_width=True)#selectbox
st.plotly_chart(count_plot, use_container_width=True)
#visualize a boxplot
box_fig = px.box(df, x='Time_of_Day', y='money', color = 'Weekday', title='Coffee Sales Distribution by Week and Time',color_discrete_sequence=px.colors.sequential.Greens)
box_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    xaxis_title='Time of Day',
    yaxis_title='Money',
)
box_plot = px.box(df, x='Time_of_Day', y='money', color = 'Weekday', title='Coffee Sales Distribution by Week and Time',color_discrete_sequence=px.colors.sequential.Greens)
box_plot.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    xaxis_title='Time of Day',
    yaxis_title='Money',
)
st.plotly_chart(box_fig, use_container_width=True)#selectbox
st.plotly_chart(box_plot, use_container_width=True)#streamlit
#pairplot to see the relationship btn variables
pair_fig = px.scatter_matrix(df,dimensions=['hour_of_day','money','Weekdaysort','Monthsort'],title = 'Pairplot for Coffeee Sales',color='Time_of_Day',color_discrete_sequence=px.colors.sequential.Greens)
pair_fig.update_traces(diagonal_visible=True)
pair_fig.update_layout(
    width=800,
    height=600,
    plot_bgcolor='white',
)
pair_plot = px.scatter_matrix(df,dimensions=['hour_of_day','money','Weekdaysort','Monthsort'],title = 'Pairplot for Coffeee Sales',color='Time_of_Day',color_discrete_sequence=px.colors.sequential.Greens)
pair_plot.update_traces(diagonal_visible=True)
pair_fig.update_layout(
    width=800,
    height=600,
    plot_bgcolor='white',
)
st.plotly_chart(pair_fig, use_container_width=True)#selectbox
st.plotly_chart(pair_plot, use_container_width=True)#streamlit
#pie chart to visualize time of day
labels = ['Morning', 'Afternoon', 'Night']
td = df['Time_of_Day'].value_counts().reset_index()
td.columns=['Time of Day','Count']
#create a dict for lookup on labels -> if we used dataframe like in seaborn it wouldnt work since it doesnt understand .get() fxn straightforwardly
td_dict = dict(zip(td['Time of Day'],td['Count']))
order = [td_dict.get(label,0) for label in labels]
pie_fig = px.pie(names=labels,values=order,title='Time of Day Distribution',color_discrete_sequence=px.colors.sequential.Greens)
pie_fig.update_layout(
    width=400,
    height=400,
)
pie_plot = px.pie(names=labels,values=order,title='Time of Day Distribution',color_discrete_sequence=px.colors.sequential.Greens)
pie_plot.update_layout(
    width=400,
    height=400,
)
st.plotly_chart(pie_fig, use_container_width=True)#selectbox
st.plotly_chart(pie_plot, use_container_width=True)#streamlit
charts = st.selectbox("Choose a chart to download",
     ['🥧Pie Chart','📊Box Plot','⏸️Pair Plot','▮Count Plot','📈Scatter Plot','🌡️Heat Map'])
if charts == '🥧Pie Chart':
        selected_fig = pie_fig
elif charts== '📊Box Plot':
    selected_fig = box_fig
elif charts == '⏸️Pair Plot':
    selected_fig = pair_fig
elif charts == '▮Count Plot':
    selected_fig = count_fig
elif charts == '📈Scatter Plot':
    selected_fig = reg_fig
elif charts == '🌡️Heat Map':
    selected_fig = heat_fig
else:
    selected_fig = None
if selected_fig:
    st.plotly_chart(selected_fig, use_container_width=True)
