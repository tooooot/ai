from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# --- Routes ---
@app.route('/', strict_slashes=False)
@app.route('/app', strict_slashes=False)
@app.route('/mobile', strict_slashes=False)
@app.route('/start', strict_slashes=False)
def mobile_app_view():
    return render_template('mobile_app.html')

@app.route('/health')
def health():
    return "FRONTEND-ONLY MODE ACTIVE"

# --- Mock APIs to prevent UI errors ---
@app.route('/api/portfolio/<strategy_name>')
def mock_portfolio(strategy_name):
    # Return dummy data matching the expected structure
    return jsonify({
        "name": strategy_name,
        "cash": 100000,
        "total_value": 150000,
        "holdings": {},
        "history": [],
        "active_trades": []
    })

@app.route('/api/chat', methods=['POST'])
def mock_chat():
    return jsonify({"response": "أنا حالياً في وضع 'العرض فقط' لتحديث النظام. سأعود للعمل قريباً!"})

@app.route('/api/live_data')
def mock_live():
    return jsonify({"leaderboard": [], "recent_trades": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
