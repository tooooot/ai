from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
@app.route('/app', strict_slashes=False)
@app.route('/mobile', strict_slashes=False)
@app.route('/health', strict_slashes=False)
def hello():
    return "<h1>FINAL CHECK: MINIMAL APP IS WORKING</h1><p>If you see this, the server is alive.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
