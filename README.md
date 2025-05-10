# 第三方支付系統
- 串接服務: `綠界科技 ECPay` 、 `LinePay`
- 開發工具
  - flask
  - blueprint
- 功能
  - 購買
  - 付款狀態確認
 
## Development
### 1. Clone this repo
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
### 2. Install the dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up environment variables
詳見 [Line Pay](https://developers-pay.line.me/zh/sandbox) & [ECPay](https://developers.ecpay.com.tw/?p=2509)
```
# General
ENV=sandbox  # or production

# Line Pay
LINEPAY_CHANNEL_ID=
LINEPAY_SECRET=

# ECPay
ECPAY_MERCHANT_ID=
ECPAY_HASH_KEY=
ECPAY_HASH_IV=
```
### 4. Start coding
Open your editor and start developing! :)

### 5. Format the code
- Format & check
    ```bash
    python format.py
    ```
- Check only (no changes)
    ```bash
    python format.py --check
    ```

### 6. Git add & commit
```bash
git add .
git commit -m "your commit message"
```

## Deployment
### Run the app with Flask
```bash
python app.py
```
### Run with Gunicorn (for production)