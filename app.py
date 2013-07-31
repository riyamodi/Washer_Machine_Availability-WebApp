from flask import Flask, render_template, redirect, request, flash, session, g, url_for
import model

app = Flask(__name__)

@app.route("/")
def index():
	