from flask import jsonify
# from flask import render_template, flash, redirect, url_for, jsonify, session
# from flask import make_response, request
from app import app
# import datetime
# from werkzeug.urls import url_parse


@app.route('/') # noqa
def home():
    return jsonify({'status': 'ok'});
