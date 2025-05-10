import datetime
import hashlib
import urllib.parse

from flask import Blueprint, render_template_string

from config import ECPAY_HASH_IV, ECPAY_HASH_KEY, ECPAY_MERCHANT_ID

ecpay_blueprint = Blueprint("ecpay", __name__)


def _generate_mac(params):
    sorted_params = sorted(params.items())
    encode_str = (
        f"HashKey={ECPAY_HASH_KEY}&"
        + "&".join([f"{k}={v}" for k, v in sorted_params])
        + f"&HashIV={ECPAY_HASH_IV}"
    )
    encode_str = urllib.parse.quote_plus(encode_str).lower()
    checksum = hashlib.sha256(encode_str.encode("utf-8")).hexdigest().upper()
    return checksum


@ecpay_blueprint.route("/checkout", methods=["POST"])
def checkout():
    now = datetime.datetime.now()
    order_params = {
        "MerchantID": ECPAY_MERCHANT_ID,
        "MerchantTradeNo": now.strftime("%Y%m%d%H%M%S"),
        "MerchantTradeDate": now.strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": "1000",
        "TradeDesc": "測試交易",
        "ItemName": "卡比巴拉商品",
        "ReturnURL": "http://127.0.0.1:5000/ecpay/return",
        "ChoosePayment": "Credit",
        "EncryptType": 1,
    }
    order_params["CheckMacValue"] = _generate_mac(order_params)

    html_form = f"""
    <form id="ecpay-form" method="post" action="https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5">
        {''.join([f'<input type="hidden" name="{k}" value="{v}"/>' for k, v in order_params.items()])}
    </form>
    <script>document.getElementById('ecpay-form').submit();</script>
    """
    return render_template_string(html_form)
