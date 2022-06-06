from flask import Flask, render_template, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/home/', methods=['GET', 'POST'])

def welcome():
    return render_template ('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)