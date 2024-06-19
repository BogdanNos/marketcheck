from flask import Flask, render_template, request, jsonify, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
import asyncio
from threading import Thread
import parser
import json 
from celery import Celery
app = Flask(__name__)
cors = CORS(app)

test_data = json.loads(open("test.json", "r", encoding='utf-8').read())

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SSL_DISABLE'] = True
#cors = CORS(app, resources={r"/punishments": {"origins": "http://*" "*"}})

#TOKEN = "zSWpKzvNLQXwIUYJph2=R5qWfQAdYvKtui9gpwZKBZJzhCkbdkMcabze0=qd0gsw6dHmLOCC4Ihumx-e5fSycfQ3?m7Q78nelJ/DbUyhUE!mQkckn1Bx8h49gt05u0I7rkACpViJtSmPsNQA=PSrt2!m0ecSmyg=Lkbi085TvLfu212IAzz?3DYFD=PeT?dHHh?S4aLS6jggw/?AUbOB?dtVtfEhm1-m46nU0NxuwdyoG4y9!8ZDTBKIfv48MbXz"

@app.route('/get_item')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_item():
    product = request.args.get('product_name')
    #sorting = request.args.get('sorting')
    #token = request.args.get("token")
    #if token != TOKEN:
    #    return "token error"
    response = parser.handle_request(product)
    print(response)
    response = jsonify(response)
    #response = jsonify({"popular" : [{"name": "megamarket", "items": [], "sorting": "popular"}, {"name": "yandex", "items": [], "sorting": "popular"}, {"name": "wildberries", "items": [], "sorting": "popular"}, {"name": "ozon", "items": [], "sorting": "popular"}],
#"price" : [{"name": "megamarket", "items": [], "sorting": "price"}, {"name": "yandex", "items": [], "sorting": "price"}, {"name": "wildberries", "items": [], "sorting": "price"}, {"name": "ozon", "items": [], "sorting": "price"}]})
    #response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', ["POST", "PUT", "PATCH", "GET", "DELETE", "OPTIONS"] )
    return response

@app.route('/test')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def test():

    return test_data

@app.route('/refresh')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def refresh():
    marketplace = request.args.get('marketplace')
    #token = request.args.get("token")
    #if token != TOKEN:
    #    return "token error"
    return parser.refresh(marketplace)
    
 
@app.route('/alive')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def ali():
    return "alive"

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', ssl_context=context) #
