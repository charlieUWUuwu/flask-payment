from flask import Flask

from ecpay import ecpay_blueprint
from linepay import linepay_blueprint

app = Flask(__name__)
app.register_blueprint(linepay_blueprint, url_prefix="/line-pay")
app.register_blueprint(ecpay_blueprint, url_prefix="/ecpay")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
