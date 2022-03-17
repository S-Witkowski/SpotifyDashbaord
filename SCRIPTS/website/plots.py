import json
import plotly
import plotly.express as px

def test_plot(df):
    fig = px.scatter(data_frame=df,
                    x='acousticness',
                    y='danceability',
                    size='popularity',
                    hover_name='trackName')
    fig.update_layout(width=1000, height=600)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def test_plot2(df):
    fig = px.pie(df, 'artistName')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
