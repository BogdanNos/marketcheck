from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
import asyncio
from threading import Thread
import parser

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SSL_DISABLE'] = False

@app.route('/get_item')
def get_item():
    product = request.args.get('product_name')
    sorting = request.args.get('sorting')
    return parser.handle_request(product, sorting)

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', ssl_context=context)