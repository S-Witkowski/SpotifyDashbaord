from sklearn.linear_model import LinearRegression
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
from sklearn.decomposition import PCA

class PlotMaker():
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def linear_regression_coef_plot(self):
        X = self.df.drop(columns=['artistName', 'trackName', 'popularity'])
        y = self.df['popularity']

        model = LinearRegression()
        model.fit(X, y)

        colors = ['Positive' if c > 0 else 'Negative' for c in model.coef_]

        fig = px.bar(
        x=X.columns, y=model.coef_, color=colors,
        color_discrete_sequence=['red', 'blue'],
        labels=dict(x='Feature', y='Linear coefficient'),
        title='Weight of each feature for predicting popularity'
        )
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    def PCA_plot(self):

        X = self.df.drop(columns=['artistName', 'trackName', 'popularity'])
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)
        fig = px.scatter(components, x=0, y=1,
            color=self.df['popularity'],
            hover_name=self.df['trackName'])

        return json.dumps(fig, cls=PlotlyJSONEncoder)

    def popularity_plot(self):
        fig = px.box(self.df, y='popularity', points='all', hover_name='trackName', height=600, width=500, title='Popularity of your songs (max 100)')
        return json.dumps(fig, cls=PlotlyJSONEncoder)
