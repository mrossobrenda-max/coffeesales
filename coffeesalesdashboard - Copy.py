import dash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dash import dcc, html, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

#load dataset
df = pd.read_csv(r"C:\Users\BRENDA\Downloads\Coffe_sales.csv")
#initialize the app
app = dash.Dash(__name__)
app.title = "Coffee Sales Dashboard"
#visuals
corr = df[['hour_of_day','money','Weekdaysort','Monthsort']].corr()
heat_fig = px.imshow(corr, text_auto='.3f',color_continuous_scale='Greens',aspect='auto',title='Correlation between time and coffee sales')
#resize the visual
heat_fig.update_layout(
    width=600,
    height=400,
)
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
#lets understand the coffeetypes sales using a countplot
coffeecount = df['coffee_name'].value_counts().reset_index()
coffeecount.columns = ['Coffee_types','Count']
count_fig = px.bar(coffeecount, x='Coffee_types', y='Count',orientation='v',title='Coffee type sales distribution',color='Count',color_continuous_scale='Greens')
count_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
)
#visualize a boxplot
box_fig = px.box(df, x='Time_of_Day', y='money', color = 'Weekday', title='Coffee Sales Distribution by Week and Time',color_discrete_sequence=px.colors.sequential.Greens)
box_fig.update_layout(
    width=600,
    height=400,
    plot_bgcolor='white',
    xaxis_title='Time of Day',
    yaxis_title='Money',
)
#pairplot to see the relationship btn variables
pair_fig = px.scatter_matrix(df,dimensions=['hour_of_day','money','Weekdaysort','Monthsort'],title = 'Pairplot for Coffeee Sales',color='Time_of_Day',color_discrete_sequence=px.colors.sequential.Greens)
pair_fig.update_traces(diagonal_visible=True)
pair_fig.update_layout(
    width=800,
    height=600,
    plot_bgcolor='white',
)
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
#layout
app.layout = html.Div([
    html.H1('☕Coffee Sales Dashboard',
                     style={'textAlign':'center','font-size':'32px'}),
    html.Div([
        #dropdown selector and a download button
        dcc.Dropdown(
            id='chart-selector',
            options=[
                {'label':'🌡️Heatmap','value':'heatmap'},
                {'label':'📈Regression','value':'regression'},
                {'label':'📊Countplot','value':'countplot'},
                {'label':'📦Boxplot','value':'boxplot'},
                {'label':'⏸️Pairplot','value':'pairplot'},
                {'label':'🥧Pie','value':'pie'},
            ],
            style={'width':'200px'}
        ),
        html.Button(children="⬇ Download Visual", id='btn-download-visual',
                    style={'backgroundColor': '#FD7E14',
                           'color': 'white',
                           'border': 'none',
                           'padding': '10px 20px',
                           'font-size': '13px',
                           'border-radius': '5px',
                           'boxShadow': '2px 2px 5px rgba(0,0,0,0.2)',
                           'margin-left': '10px',
                           }),
        dcc.Download(id="download-component"),#this enables the actual download of the visual
 ], style={'display':'flex','justifyContent':'flex-end','alignItems':'center'}),
    dcc.Loading(id = "loading_message", type = "circle", className='custom-spinner',
                children=[html.Button(children= "📃Download Full Report", id='btn-download-full-report',
                style={'backgroundColor': '#198754',
                       'color': 'white',
                       'border': 'none',
                       'padding': '10px 20px',
                       'font-size': '13px',
                       'border-radius': '5px',
                       'boxShadow': '2px 2px 5px rgba(0,0,0,0.2)',
                       'margin-left': '10px',
                       'cursor': 'pointer',
                       }),
                html.Div(id = "download-status"),
    dcc.Download(id="download-report")]), #this enables the full download of the report
    html.Div([
        html.Div([
            dcc.Graph(figure=heat_fig)
        ]),
        html.Div([
             dcc.Graph(figure=reg_fig)
        ])
    ], style={
        'display':'flex','justify-content': 'space-between'
    }),
    html.Div([
        html.Div([
            dcc.Graph(figure=count_fig)
        ]),
        html.Div([
            dcc.Graph(figure=box_fig)
        ])
    ], style={
        'display':'flex','justify-content': 'space-between'
    }),
    html.Div([
        html.Div([
            dcc.Graph(figure=pair_fig)
        ]),
        html.Div([
            dcc.Graph(figure=pie_fig)
        ])
    ], style={
        'display':'flex','justify-content': 'space-between'
    })
])
#app callback
@app.callback(
    Output('download-component', 'data'),
    Input('btn-download-visual', 'n_clicks'),
    State('chart-selector', 'value'),
    prevent_initial_call=True
)
#define a fxn tht will iterate thru the values-selected figures accordingly
def download_selected_chart(n_clicks, selected_chart):
    if selected_chart == 'heatmap':
        fig = heat_fig
    elif selected_chart == 'regression':
        fig = reg_fig
    elif selected_chart == 'countplot':
        fig = count_fig
    elif selected_chart == 'boxplot':
        fig = box_fig
    elif selected_chart == 'pairplot':
        fig = pair_fig
    elif selected_chart == 'pie':
        fig = pie_fig
    else:
        return None #fallback if no match
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png')
    buffer.seek(0)
    return dcc.send_bytes(buffer.read(),filename=f'{selected_chart}.png')
#app callback for downloading full report
@app.callback(
    Output('download-report', 'data'),
    Output('download-status', 'children'),
    Input('btn-download-full-report', 'n_clicks'),
    prevent_initial_call=True
)
#defn a function that will iterate through the visuals send/write them to the buffer before download of report
def download_fullreport (n_clicks):
    #...PDF loading sms..
    message = "📥Your report is ready for download."
    #step 1 we create a dictionary to hold our visuals
    chart_maps = {
        'HeatMap': heat_fig,
        'Regression': reg_fig,
        'Countplot': count_fig,
        'BoxPlot': box_fig,
        'Pairplot': pair_fig,
        'PieChart': pie_fig
    }
    #create a list
    # use a for loop to iterate through the dict items and  write them to the buffer
    chart_images = []
    for name, fig in chart_maps.items():
        buffer = io.BytesIO()
        fig.write_image(buffer, format='png')
        buffer.seek(0)
        chart_images.append((name,buffer.read())) #append only takes 1 variable
        # so we use a tuple to hold the name and buffered visuals
    #create a PDF in memory
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer)
    styles = getSampleStyleSheet()
    element = [
        Paragraph('☕Coffee Sales Dashboard Report', styles['Title']),
        Spacer(1, 12)
    ]
    #iterate the visuals and write to pdf
    for name, img_bytes in chart_images:
        img_buffer = io.BytesIO(img_bytes)
        element.append(Paragraph(name, styles['Heading2']))
        element.append(Image(img_buffer,width=400, height=300))
        element.append(Spacer(1, 12))
        #write to pdf
    doc.build(element)
    pdf_buffer.seek(0)
    return dcc.send_bytes(pdf_buffer.read(),filename = 'Coffee Sales Dashboard Report.pdf'),message

#run the main app))
if __name__ == '__main__':
    app.run(debug=True,port=8080)
