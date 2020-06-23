#!/usr/bin/env python3

##################################################
# Title:    Market Stocks Selection System
# Author:   Brandon Rickman <brandon.rickman@snhu.edu>
# Desc:     Runs varies CRUD commands on specified database using PyMongo
# Revised:  Web App used for CS499 Database Capstone
##################################################

__author__ = "Brandon Rickman"
__version__ = "1.1.0"

'''
---------------------------------
NOTES
---------------------------------
To run this application:
- install MongoDB and load stocks.json
use [python3 stocks_s3.py], [flask run] should work but
I was not able to get it to run during development using flask run.

Flask uses port 5000 to run web apps, I did not change this, however if you
want to use port 8080 add param to app.run(port=8080) in dunder name at the 
bottom.
---------------------------------
'''

# Libraries
import sys, json
from pymongo import MongoClient, ASCENDING, DESCENDING
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo 
from bson import Binary, Code
from bson.json_util import dumps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# Flask build section
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/market.db"
app.config['SECRET_KEY'] = 'f23b46913e225841749d86111eff3585'
mongo = PyMongo(app)

# Estabilish mongoDB connection
connection = MongoClient('localhost', 27017)
# Define MongoDB and Collection "market.stocks"
db = connection['market'] 
collection = db['stocks']

# Routes
baseURL = '/stocks/api/v1.1'


# Home page URL
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Documentation')


class StockForm(FlaskForm):
    ticker = StringField('Ticker', validators = [DataRequired(), Length(min=1, max=5)])
    submit = SubmitField('Search')


def searchStock(ticker):
    try:
        query = {"Ticker": ticker}
        result = collection.find(query)

        # Notify user of success/failure of reading the docutment
        if result:
            result = dumps(result)
        else:
            result = "No matching record found."
    
    except:
        result = "Oops, something went wrong."
    
    finally:
        return result

'''
@app.route('/search', methods=['GET'])
def search():
    form = StockForm()
    data = searchStock(form.ticker)
    if form.validate_on_submit():
        info = f'Account created for {data}!'
        return info
    return render_template('search.html', title='Search', form=form)
'''

@app.route('/search', methods=['GET'])
def search():
    a = request.args.get('a')
    if (a == ''):
        return 'Invalid entry please try again.'
    else:
        c = json.dumps(a.__dict__)
        return c


# Create a Stock URI
@app.route(baseURL + '/setStock', methods=['POST'])
def setStock():
    try:
        # Create doc on JSON request
        result = collection.insert_one(request.json)
        # Notify user of success/failure to create a new docutment by ID number
        if result.inserted_id:
            msg = f"Document successfully created as id: {result.inserted_id}"
        else:
            msg = "Document creation failed"

    except:
        msg = "Oops, something went wrong"

    finally:
        return msg


# Read a Stock URI
@app.route(baseURL + '/getStock/<ticker>')
def getStock(ticker):
    try:
        query = {"Ticker": ticker}
        result = collection.find(query)

        # Notify user of success/failure of reading the docutment
        if result:
            result = dumps(result)
        else:
            result = "No matching record found."
    
    except:
        result = "Oops, something went wrong."
    
    finally:
        return result


# Update a Stock URI
@app.route(baseURL + '/updateStock/<ticker>', methods=['PUT'])
def updateStock(ticker):
    try:
        query = {"Ticker": ticker}
        new = {"$set": request.json}
        result = collection.update_one(query, new)

        # Notify user of success/failure of updated docutment
        if result.modified_count > 0:
            result = f"{result.modified_count} record(s) updated."
        else:
            result = "No records updated."
    
    except:
        result = "Oops, something went wrong."
    
    finally:
        return result


# Delete a Stock URI
@app.route(baseURL + '/deleteStock/<ticker>', methods=['DELETE'])
def deleteStock(ticker):
    try:
        query = {"Ticker": ticker}
        result = collection.delete_one(query)

        # Notify user of success/failure of deletion of the docutment
        if result.deleted_count > 0:
            result = f"{result.deleted_count} record(s) deleted."
        else:
            result = "No records deleted."
    
    except:
        result = "Oops, something went wrong."
    
    finally:
        return result


# Stock Report summary based on price, change from open, and volume
@app.route(baseURL + '/stockReport', methods=['POST'])
def stockReport():
    try:
        r = request.json
        stocks = []
        for ticker in r['ticker']:
            stocks.append(collection.find_one({'Ticker': ticker}, {'_id': 0, 'Ticker': 1, 'Price': 1, "Change from Open": 1, "Volume": 1}))
        return {"report": stocks}
    except:
        return "Oops, something went wrong."


# Top 5 Stocks by Industry performance
@app.route(baseURL + '/industryReport/<industry>')
def industryReport(industry):
    try:
        query = {'Industry': industry}
        top5 = dumps(collection.find(query).sort("Performance (YTD)", DESCENDING).limit(5))
        return top5
    except:
        return "Oops, something went wrong."


# Main program function
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
