#!/usr/bin/env python3

from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session
from dotenv import load_dotenv
import psycopg2
import os
import json

app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

try:
    conn = psycopg2.connect(DATABASE_URL)
except:
    print('Can`t establish connection to database')


@app.get('/')
def index():
    term = request.args.get('url', '', type=str)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        h1 = "Анализатор страниц",
        messages=messages,
        search=term
    )


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
