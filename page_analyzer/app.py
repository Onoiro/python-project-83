#!/usr/bin/env python3

from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session
                  
import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    term = request.args.get('url', '', type=str)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages,
        search=term
    )


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
