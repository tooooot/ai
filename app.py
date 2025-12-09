from flask import Flask, render_template, jsonify
from config import Config
from market_data import MarketDataService
from news_engine import NewsEngine
from portfolio_manager import PortfolioManager
from ai_trader import AITrader
from challenge_engine import ChallengeEngine
import threading
import time
import random

app = Flask(__name__)
app.config.from_object(Config)

@app.errorhandler(404)
def page_not_found(e):
    # Debug: Print all active routes
    output = "<h1>404 - Not Found</h1><p>Active Routes:</p><ul>"
    for rule in app.url_map.iter_rules():
        output += f"<li>{rule}</li>"
    output += "</ul>"
    return output, 404

@app.route('/design_gallery')
def design_gallery():
    return render_template('design_gallery.html')

# --- Services Initialization ---
market_service = MarketDataService()
news_service = NewsEngine()
portfolio_manager = PortfolioManager()
ai_trader = AITrader(market_service, news_service)
challenge_engine = ChallengeEngine(portfolio_manager)

# --- Simulation Loop ---
def simulation_loop():
    """
    Background thread to simulate the market and AI decisions.
    """
    print("Starting Simulation Loop...")
    challenge_engine.start_new_week()
    
    while True:
        try:
            # 1. Update Market Status
            # In real app, we fetch new prices here for all tracked symbols
            
            # 2. AI Decision Making (Randomly pick a strategy to act per tick)
            strategies = list(portfolio_manager.portfolios.keys())
            active_strategy = random.choice(strategies)
            
            portfolio_state = portfolio_manager.portfolios[active_strategy]
            decision = ai_trader.get_decision(active_strategy, portfolio_state)
            
            if decision:
                # Always log the reasoning, whether BUY, SELL, or HOLD
                portfolio_manager.update_log(active_strategy, f"[{decision['action']}] {decision.get('reason', '')}")
            
            if decision and decision['action'] == 'BUY':
                # Execute Buy
                success, msg = portfolio_manager.execute_trade(
                    active_strategy, 'BUY', decision['symbol'], 
                    decision['price'], decision['quantity'], 
                    decision['reason'], decision['goals'],
                    extra_data=decision
                )
                if success:
                    print(f"TRADE: {active_strategy} Bought {decision['symbol']}")
            
            # 3. Simulated Price Movements & Stop Loss/Take Profit Checks
            # (Simplified for demo)
            for name, p in portfolio_manager.portfolios.items():
                # Re-calculate total value based on mock price updates or real if available
                current_val = p['cash']
                for sym, qty in p['holdings'].items():
                    price = market_service.get_current_price(sym)
                    if price:
                        current_val += price * qty
                        
                        # Check Stops/Targets for active trades (basic check)
                        # In a full implementation, we'd map trades to specific lots
                        for trade in p['active_trades']:
                            if trade['symbol'] == sym and trade['goals']:
                                if price >= trade['goals']['target_price']:
                                    # Take Profit
                                    portfolio_manager.execute_trade(name, 'SELL', sym, price, qty, "Target Reached", None, {})
                                elif price <= trade['goals']['stop_loss']:
                                    # Stop Loss
                                    portfolio_manager.execute_trade(name, 'SELL', sym, price, qty, "Stop Loss Hit", None, {})

                p['total_value'] = current_val

            challenge_engine.check_status()
            
            time.sleep(5) # Tick every 5 seconds
            
        except Exception as e:
            print(f"Simulation Error: {e}")
            time.sleep(5)

# Start Simulation Thread
sim_thread = threading.Thread(target=simulation_loop, daemon=True)
sim_thread.start()

# --- Routes ---

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/health')
def health_check():
    return "App is Running! V-DEBUG-2"

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/live')
def live_broadcast():
    return render_template('live.html')

@app.route('/app', strict_slashes=False)
@app.route('/mobile', strict_slashes=False)
@app.route('/start', strict_slashes=False)
def mobile_app_view():
    return render_template('mobile_app.html')

@app.route('/debug/routes')
def debug_routes():
    return str(app.url_map)

@app.route('/verify')
def verify_view():
    return render_template('verify.html')

@app.route('/test-devices')
def device_lab():
    return render_template('test_devices.html')

# --- API Endpoints ---

@app.route('/api/live_data')
def api_live_data():
    """
    Returns data for the Live Broadcast view.
    Includes Leaderboard and latest Ticker events.
    """
    leaderboard = portfolio_manager.get_portfolio_summary()
    
    # Get latest 5 trades across all portfolios
    latest_trades = []
    for name, p in portfolio_manager.portfolios.items():
        for trade in p['history'][-2:]: # Last 2 per strategy
            trade_display = trade.copy()
            trade_display['strategy'] = name
            latest_trades.append(trade_display)
            
    # Sort trades by timestamp (mock timestamp for now, assume order is roughly correct)
    # In real app, use real datetime objects
    
    return jsonify({
        "leaderboard": leaderboard,
        "recent_trades": latest_trades[-10:] # Return last 10 global trades
    })

@app.route('/api/portfolio/<strategy_name>')
def api_portfolio_detail(strategy_name):
    """
    Returns full details for the App view.
    """
    portfolio = portfolio_manager.portfolios.get(strategy_name)
    if portfolio:
        return jsonify(portfolio)
    return jsonify({"error": "Not Found"}), 404

@app.route('/api/news_archive')
def api_news_archive():
    return jsonify(news_service.get_archive())

@app.route('/api/verify_data')
def api_verify_data():
    """
    Returns metadata for verification page.
    """
    # Default to "Meqdam" for the main verified view if no param
    from flask import request
    strategy = request.args.get('strategy', 'مقدام')
    
    audit_data = portfolio_manager.get_audit_report(strategy)
    
    if not audit_data:
        # Fallback
        return jsonify({"error": "Strategy not found"}), 404
        
    return jsonify({
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "market_status": "Open (Simulated)", 
        "connection_status": "Healthy",
        "data_source": "yfinance + Tadawul (Live Connection)",
        "audit": audit_data
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    from flask import request
    data = request.json
    ui_persona = data.get('persona', 'General')
    message = data.get('message', '')
    
    # Simple Simulated AI Response Engine
    # In a real app, this would call OpenAI/Gemini
    
    # Contextual Response Logic
    portfolio = portfolio_manager.portfolios.get(ui_persona)
    last_trade = portfolio['history'][-1] if portfolio and portfolio['history'] else None
    
    # Check if user is questioning decisions
    is_questioning = any(w in message for w in ["ليش", "لماذا", "سبب", "غلط", "خطأ", "تسرعت"])
    
    if is_questioning and last_trade:
        # Smart Response based on last action
        reason = last_trade.get('reason', 'ظروف السوق كانت مناسبة.')
        symbol = last_trade.get('symbol', 'السهم')
        action = "شراء" if last_trade.get('action') == "BUY" else "بيع"
        
        response_text = f"سؤال وجيه. قراري بـ {action} {symbol} كان مدروساً. السبب: {reason}. أنا ألتزم بالخطة."
        
    else:
        # Personality Fallback
        if "قناص" in ui_persona:
            responses = [
                "نحن لا نلاحق السهم، ننتظره يأتي إلينا عند القاع.",
                "مؤشر RSI منخفض جداً.. رائحة الارتداد تفوح.",
                "الصبر هو سلاح القناص.. انتظر اللحظة المناسبة.",
                "رأيت تشبعاً بيعياً واضحاً.. الدخول الآن آمن نسبياً."
            ]
            response_text = random.choice(responses)

        elif "موج" in ui_persona:
            responses = [
                "الاتجاه هو صديقي المفضل.. والنهر يجري للأعلى.",
                "لا تعاند السوق.. اركب الموجة واستمتع بالرحلة.",
                "المتوسطات تتقاطع إيجابياً.. إشارة دخول قوية.",
                "نحن نشتري القوة ونبيع الضعف."
            ]
            response_text = random.choice(responses)

        elif "برق" in ui_persona:
            responses = [
                "بسرعة! فرصة مضاربية لا تعوض.. خروج بعد دقيقتين!",
                "اضرب واهرب.. السوق لا يرحم البطيئين.",
                "حركة السعر (Price Action) تقول: انفجار وشيك!",
                "لا يهمني اسم الشركة.. يهمني حركة السهم الآن."
            ]
            response_text = random.choice(responses)

        elif "حصاد" in ui_persona:
            responses = [
                "قطرة قطرة يمتلئ النهر.. نبحث عن التوزيعات المستمرة.",
                "النمو البطيء والمستمر خير من الربح السريع والمخاطر.",
                "هل توزع الشركة أرباحاً؟ هذا هو سؤالي الوحيد.",
                "استثمار طويل الأجل.. فاترك الشاشة واذهب للنوم."
            ]
            response_text = random.choice(responses)

        elif "مقتحم" in ui_persona:
            responses = [
                "السيولة تقتحم السهم بقوة! سأدخل مع الهوامير.",
                "كسرنا حاجز مقاومة عنيد.. الطريق مفتوح للأعلى.",
                "رالي صعودي قوي.. لا تكن متفرجاً.",
                "السيولة الذكية دخلت.. ونحن خلفها مباشرة."
            ]
            response_text = random.choice(responses)

        elif "جوال" in ui_persona:
            responses = [
                "قطاع الاسمنتات نائم.. لكن البتروكيماويات يشتعل!",
                "أبحث عن القطاع الذي لم يرتفع بعد.. هناك الفرص.",
                "السيولة تدور بين القطاعات.. وأنا أسبقها بخطوة.",
                "التنويع بين القطاعات هو سر النجاة."
            ]
            response_text = random.choice(responses)
            
        elif "رزين" in ui_persona:
             responses = [
                "يا بني، العجلة من الشيطان. نحن نشتري الأسهم ذات العوائد وننام عليها.",
                "السوق يمر بموجات، والعاقل من يمسك الكاش ليوم الفرص.",
                "هل اطلعت على مكرر الربحية لهذا السهم؟ لا تغرك الارتفاعات الوهمية.",
                "الأمان قبل الأرباح.. هذه قاعدتي الذهبية."
            ]
             response_text = random.choice(responses)
            
        elif "عواطف" in ui_persona:
            responses = [
                "يا الله! شفت الخبر اللي نزل قبل شوي؟ السوق مولع! 🔥",
                "إحساسي يقول السهم هذا بيطير.. تويتر كله يتكلم عنه!",
                "لا تكون خاوف.. الفرص تموت إذا فكرنا واجد.",
                "أحب اللون الأخضر! 💚"
            ]
            response_text = random.choice(responses)
            
        elif "مقدام" in ui_persona:
            responses = [
                "لا وقت للراحة! الحجم عالي والسيولة تتدفق.. ادخل الآن!",
                "نحن هنا لنصنع الثروة، ليس لنحفظها.",
                "انظر للشارت.. نموذج كوب وعروة مثالي يتشكل.",
                "الهجوم خير وسيلة للدفاع."
            ]
            response_text = random.choice(responses)
            
        elif "محظوظ" in ui_persona:
            responses = [
                "والله مدري.. حسيت الرقم 7 حلو اليوم وشريت.",
                "رميت العملة وطلعت صورة.. يعني شراء!",
                "التحليل الفني؟ خرابيط.. الحظ هو الملك.",
                "دع الأمور تمشي كما كتب لها."
            ]
            response_text = random.choice(responses)
            
        else:
            response_text = f"أنا {ui_persona}.. أحلل البيانات بدقة لاتخاذ القرار."

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
