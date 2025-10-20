# =========================
# 🔧 CONFIGURAÇÕES (config.py)
# =========================
NUVEMSHOP_CLIENT_ID = "SEU_CLIENT_ID"
NUVEMSHOP_CLIENT_SECRET = "SEU_CLIENT_SECRET"
NUVEMSHOP_REDIRECT_URI = "https://SEUSITE.com.br/oauth/callback"

FACEBOOK_APP_ID = "SEU_FACEBOOK_APP_ID"
FACEBOOK_APP_SECRET = "SEU_FACEBOOK_APP_SECRET"
FACEBOOK_PAGE_ID = "SUA_PAGE_ID"
FACEBOOK_ACCESS_TOKEN = "SEU_TOKEN_DE_PAGINA"

# =========================
# 🚀 IMPORTAÇÕES
# =========================
from flask import Flask, request
import requests

app = Flask(__name__)

# =========================
# 🔐 AUTENTICAÇÃO NUVEMSHOP (nuvemshop.py)
# =========================
@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    token_url = "https://www.nuvemshop.com.br/apps/oauth/token"
    payload = {
        "client_id": NUVEMSHOP_CLIENT_ID,
        "client_secret": NUVEMSHOP_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": NUVEMSHOP_REDIRECT_URI
    }
    response = requests.post(token_url, json=payload)
    access_token = response.json().get("access_token")
    return f"✅ Token recebido com sucesso: {access_token}"

# =========================
# 📦 PUBLICAÇÃO NO FACEBOOK (facebook.py)
# =========================
def post_product_to_facebook(title, image_url, link):
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "caption": f"{title}\nCompre agora: {link}",
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

# =========================
# 📬 WEBHOOKS LGPD E PRODUTOS (webhook.py)
# =========================
@app.route("/webhook/customers-created", methods=["POST"])
def handle_customer_created():
    data = request.json
    print("👤 Novo cliente criado:", data)
    return "OK", 200

@app.route("/webhook/customers-data-request", methods=["POST"])
def handle_data_request():
    data = request.json
    print("📄 Solicitação LGPD:", data)
    return "OK", 200

@app.route("/webhook/product-created", methods=["POST"])
def handle_product_created():
    data = request.json
    title = data.get("name")
    image_url = data.get("images", [{}])[0].get("src")
    link = data.get("url")
    if title and image_url and link:
        result = post_product_to_facebook(title, image_url, link)
        print("📢 Produto publicado:", result)
        return "Publicado com sucesso", 200
    else:
        return "Dados incompletos", 400

# =========================
# 🏠 ROTA PRINCIPAL
# =========================
@app.route("/")
def home():
    return "🚀 Bot de Postagem Automática Nuvemshop + Facebook está rodando!"

# =========================
# ▶️ EXECUÇÃO LOCAL
# =========================
if __name__ == "__main__":
    app.run(debug=True)