from flask import Blueprint, render_template, request, redirect, url_for, session, flash

import flask_excel as excel
from .data_downloader import SpotifyData
from .dashboard.dashboard_main import PlotMaker
from spotipy import SpotifyOauthError


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session.clear()
        playlist_link = request.form['link']
        try:
            spotify_data = SpotifyData(playlist_link)
        except:
            flash('Auth problem.') 
            return render_template('home.html')
            
        data = spotify_data.download_data()
        if data:
            session['data'] = data
            return redirect(url_for('views.dashboard'))
        else:
            flash('Wrong link for playlist passed. Try another one.')
            return render_template('home.html')
    else:
        return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/dashboard')
def dashboard():
    if 'data' in session:
        data = session['data']
        pm = PlotMaker(data)
        return render_template('dashboard.html',
            pop_plot = pm.popularity_plot(),
            data=pm.linear_regression_coef_plot(),
            data2=pm.PCA_plot()
            )
    else:
        return render_template('no_data.html')

@views.route('/dashboard/export', methods=['GET'])
def export_data():
    if 'data' in session:
        return excel.make_response_from_records(session['data'], 'csv', file_name='exported_spotify_data')
    else:
        return render_template('no_data.html')