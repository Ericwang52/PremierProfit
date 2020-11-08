from flask import Flask,request,redirect, url_for, render_template
import requests
import sys, time
import re
import os
import test

app = Flask(__name__)
app.config["DEBUG"] = True
app.static_folder = 'static'

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/predict.html', methods=['GET'])
def predict():
    return render_template("predict.html")

@app.route('/about.html', methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/next.html", methods=['GET'])
def next():
    return render_template("next.html", home=request.args['home'])

@app.route('/results.html', methods=['GET'])
def results():
    if 'home' in request.args:
        home = (request.args['home'])
    else:
        return "Error: No home team provided. Please specify."
    if 'away' in request.args:
        away = (request.args['away'])
    else:
        return "Error: No away team provided. Please specify."
    home=home.replace("'","")
    print(home)
    output=test.getOdds(home, away)
    return render_template('results.html', lose=100*output[0][0], draw=100*output[0][1], win=100*output[0][2])
    
if __name__ == '__main__':
    app.run()