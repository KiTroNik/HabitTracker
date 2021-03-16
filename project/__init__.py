from flask import Flask, render_template
from project.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.route('/')
def hello_world():
    return render_template('index.html')
