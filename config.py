import os

from dotenv import load_dotenv

load_dotenv()

# General
ENV = os.getenv("ENV", "sandbox")

# LINE PAY
LINEPAY_CHANNEL_ID = os.getenv("LINEPAY_CHANNEL_ID")
LINEPAY_SECRET = os.getenv("LINEPAY_SECRET")
LINEPAY_GATEWAY_URL = (
    "https://sandbox-api-pay.line.me" if ENV == "sandbox" else "https://api-pay.line.me"
)

# ECPay
ECPAY_MERCHANT_ID = os.getenv("ECPAY_MERCHANT_ID")
ECPAY_HASH_KEY = os.getenv("ECPAY_HASH_KEY")
ECPAY_HASH_IV = os.getenv("ECPAY_HASH_IV")
ECPAY_GATEWAY_URL = (
    "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
    if ENV == "sandbox"
    else "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5"
)
