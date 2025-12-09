from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/health')
@app.route('/app')
@app.route('/mobile')
def hello():
    return "MINIMAL APP WORKS! The issue was dependencies."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
