from flask import Flask, url_for, render_template
import json
import os
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    filepath = os.path.abspath(os.path.dirname(__file__))
    filepath += '/static/beauty_data.json'
    with open(file=filepath, mode='r', encoding='UTF-8') as f:
        pic_data = json.loads(f.read())
    for idx, pic in enumerate(pic_data):
        pic['id'] = idx
    return render_template('index.html', pic_data=pic_data)


@app.route('/album/<int:id>')
def album(id):
    filepath = os.path.abspath(os.path.dirname(__file__))
    filepath += '/static/beauty_data.json'
    with open(file=filepath, mode='r', encoding='UTF-8') as f:
        pic_data = json.loads(f.read())
    for idx, pic in enumerate(pic_data):
        pic['id'] = idx
    return render_template('album.html', pic_data=pic_data[id])


if __name__ == '__main__':
    app.debug = True
    app.run()