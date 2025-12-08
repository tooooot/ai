import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'saudi-stock-ai-challenge-2025'
    DEBUG = True
    # Simulation Settings
    INITIAL_CAPITAL = 100000.0  # SAR
    COMMISSION_RATE = 0.00155   # Standard Saudi Market Commission (approx)
    TAX_RATE = 0.15             # VAT on Commission
