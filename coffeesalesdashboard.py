import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import plotly.io as pio
from fpdf import FPDF
#load dataset
df = pd.read_csv("data/Coffe_sales.csv")
#streamlit
st.title("☕Coffee Sales Dashboard")
st.subheader("Analytical Summary")
#visuals
#functions to cater for report downloads
def createheatmap(df):
    corr = df[['hour_of_day', 'money', 'Weekdaysort', 'Monthsort']].corr()
    fig = px.imshow(corr, text_auto='.3f', color_continuous_scale='Greens', aspect='auto',
                         title='Correlation between time and coffee sales')
    # resize the visual
    fig.update_layout(
        width=600,
        height=400,
    )
    return fig
def createregplot(df):
    x = df['money']
    y = df['hour_of_day']
    # regplot to show correlation btn sales and hourofday
    coeffs = np.polyfit(x, y, 1)
    regline = np.poly1d(coeffs)
    x_range = np.linspace(x.min(), x.max(), 20)
    ypred = regline(x_range)
    # create the scatter/regplot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=ypred, mode='markers', name='Coffee Sales', marker=dict(color='green')))  # scatter datapoints
    fig.add_trace(
        go.Scatter(x=x_range, y=ypred, mode='lines', name='Hours of Day', line=dict(color='green')))  # regression line
    fig.update_layout(
        width=600,
        height=400,
        plot_bgcolor='white',
        title='How hour of the day affects the Coffee sales',
        xaxis_title='Sales',
        yaxis_title='Hour of Day',
        colorway=['#ff0000', '#00ff00', '#0000ff'],
    )
    return fig
def createcountplot(df):
    coffeecount = df['coffee_name'].value_counts().reset_index()
    coffeecount.columns = ['Coffee_types', 'Count']
    fig = px.bar(coffeecount, x='Coffee_types', y='Count', orientation='v',
                       title='Coffee type sales distribution', color='Count', color_continuous_scale='Greens')
    fig.update_layout(
        width=600,
        height=400,
        plot_bgcolor='white',
    )
    return fig
def createboxplot(df):
    fig = px.box(df, x='Time_of_Day', y='money', color='Weekday',
                     title='Coffee Sales Distribution by Week and Time',
                     color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_layout(
        width=600,
        height=400,
        plot_bgcolor='white',
        xaxis_title='Time of Day',
        yaxis_title='Money',
    )
    return fig
def createpairplot(df):
    fig = px.scatter_matrix(df, dimensions=['hour_of_day', 'money', 'Weekdaysort', 'Monthsort'],
                                 title='Pairplot for Coffeee Sales', color='Time_of_Day',
                                 color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_traces(diagonal_visible=True)
    fig.update_layout(
        width=800,
        height=600,
        plot_bgcolor='white',
    )
    return fig
def createpiechart(df):
    labels = ['Morning', 'Afternoon', 'Night']
    td = df['Time_of_Day'].value_counts().reset_index()
    td.columns = ['Time of Day', 'Count']
    # create a dict for lookup on labels -> if we used dataframe like in seaborn it wouldnt work since it doesnt understand .get() fxn straightforwardly
    td_dict = dict(zip(td['Time of Day'], td['Count']))
    order = [td_dict.get(label, 0) for label in labels]
    fig = px.pie(names=labels, values=order, title='Time of Day Distribution',
                     color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_layout(
        width=400,
        height=400,
    )
    return fig
corr = df[['hour_of_day','money','Weekdaysort','Monthsort']].corr()
heat_fig = px.imshow(corr, text_auto='.3f',color_continuous_scale='Greens',aspect='auto',title='Correlation between time and coffee sales')
#resize the visual
heat_fig.update_layout(
    width=600,
    height=400,
)
st.plotly_chart(heat_fig, use_container_width=True)
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
st.plotly_chart(reg_fig, use_container_width=True)
#lets understand the coffeetypes sales using a countplot
coffeecount = df['coffee_name'].value_counts().reset_index()
coffeecount.columns = ['Coffee_types','Count']
count_fig = px.bar(coffeecount, x='Coffee_types', y='Count',orientation='v',title='Coffee type sales distribution',color='Count',color_continuous_scale='Greens')
count_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
st.plotly_chart(count_fig, use_container_width=True)
#visualize a boxplot
box_fig = px.box(df, x='Time_of_Day', y='money', color = 'Weekday', title='Coffee Sales Distribution by Week and Time',color_discrete_sequence=px.colors.sequential.Greens)
box_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    xaxis_title='Time of Day',
    yaxis_title='Money',
)
st.plotly_chart(box_fig, use_container_width=True)
#pairplot to see the relationship btn variables
pair_fig = px.scatter_matrix(df,dimensions=['hour_of_day','money','Weekdaysort','Monthsort'],title = 'Pairplot for Coffeee Sales',color='Time_of_Day',color_discrete_sequence=px.colors.sequential.Greens)
pair_fig.update_traces(diagonal_visible=True)
pair_fig.update_layout(
    width=800,
    height=600,
    plot_bgcolor='white',
)
st.plotly_chart(pair_fig, use_container_width=True)
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
st.plotly_chart(pie_fig, use_container_width=True)
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
    st.download_button("⬇️ Download Chart as HTML", selected_fig.to_html(), file_name="chart.html")
if st.button("📄 Generate Full PDF Report"):
    with st.spinner("Generating report..."):
        # Save fresh copies of each chart
        createheatmap(df).write_image("heatmap.png")
        createregplot(df).write_image("regression.png")
        createcountplot(df).write_image("countdistribution.png")
        createboxplot(df).write_image("boxplot.png")
        createpairplot(df).write_image("pairplot.png")
        createpiechart(df).write_image("piechart.png")
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for img in [
            "heatmap.png", "regression.png", "countdistribution.png",
            "boxplot.png", "pairplot.png", "piechart.png"
        ]:
            pdf.image(img, x=10, w=180)  # Adjust width to fit page
        pdf.output("coffeesalesdashboard.pdf")
        # Offer download
        with open("coffeesalesdashboard.pdf", "rb") as f:
            st.download_button(
                label="📥 Download Full Report",
                data=f,
                file_name="Coffee_Sales_Report.pdf",
                mime="application/pdf"
            )
