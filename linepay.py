import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timedelta

import requests
from flask import Blueprint, jsonify, request

from config import LINEPAY_CHANNEL_ID, LINEPAY_GATEWAY_URL, LINEPAY_SECRET

linepay_blueprint = Blueprint("line-pay", __name__)


def _generate_headers(body_json, channel_secret, url):
    nonce = str(uuid.uuid4())
    string_to_sign = f"{channel_secret}{url}{body_json}{nonce}"
    binary_message = string_to_sign.encode()
    binary_secret_key = channel_secret.encode()
    hash = hmac.new(binary_secret_key, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()
    return {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": LINEPAY_CHANNEL_ID,
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }


@linepay_blueprint.route("/line-pay/request", methods=["GET"])
def request_payment():
    url = "/v3/payments/request"
    request_url = f"{LINEPAY_GATEWAY_URL}{url}"
    products_quantity = 1  # 購買的商品數量
    products_price = 30  # 購買單價
    order_id = datetime.utcnow() + timedelta(hours=8)
    order_id = order_id.strftime("%Y%m%d%H%M%S")  # 訂單編號

    body = {
        "amount": products_price * products_quantity,  # 總額
        "currency": "TWD",
        "orderId": order_id,
        "packages": [
            {
                "id": "kapybara",  # 系列名或分店名
                "amount": products_price * products_quantity,
                "products": [
                    {
                        "id": "keychain",  # 商品內部名
                        "name": "卡比巴拉-鑰匙圈",  # 呈現給消費者看的商品名
                        "imageUrl": "https://sticker.png",  # 商品圖片
                        "quantity": products_quantity,  # 商品數量
                        "price": products_price,  # 商品單價
                    },
                ],
            },
        ],
        "options": {"display": {"locale": "zh_TW"}},
        "redirectUrls": {
            "confirmUrl": "http://127.0.0.1:5000/line-pay/confirm",  # 付款成功
            "cancelUrl": "https://example.com.tw/line-pay/cancel/",  # 付款失敗
        },
    }

    body_json = json.dumps(body)
    headers = _generate_headers(body_json, LINEPAY_SECRET, url)
    response = requests.post(request_url, headers=headers, data=body_json)
    data = response.json()

    if data.get("returnCode") == "0000":  # 成功代碼
        return jsonify({"paymenturl": data["info"]["paymentUrl"]}), 200
    else:
        return (
            jsonify({"detail": f"request to LINE failed: {data.get('returnCode')}"}),
            500,
        )


@linepay_blueprint.route("/line-pay/confirm", methods=["GET"])
def confirm_payment():
    # 再次確認消費者是否真的付款成功，而非餘額不足/跳掉網頁/刷卡失敗等情況
    transaction_id = request.args.get("transactionId")
    order_id = request.args.get("orderId")

    if not transaction_id or not order_id:
        return jsonify({"detail": "Missing transactionId or orderId"}), 400

    url = f"/v3/payments/{transaction_id}/confirm"
    request_url = f"{LINEPAY_GATEWAY_URL}{url}"

    body = {
        "amount": 30,
        "currency": "TWD",
    }
    body_json = json.dumps(body)

    headers = _generate_headers(body_json, LINEPAY_SECRET, url)
    response = requests.post(request_url, headers=headers, data=body_json)
    data = response.json()

    if data.get("returnCode") == "0000":
        return jsonify({"detail": "付款成功"}), 200
    elif data.get("returnCode") == "1172":
        return jsonify({"detail": "1172 transaction repeat!"}), 500
    else:
        return (
            jsonify({"detail": f"confirm to LINE failed: {data.get('returnCode')}"}),
            500,
        )
