from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session

import os
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello User!'


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
