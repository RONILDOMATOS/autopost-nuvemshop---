from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# 🔧 CONFIGURAÇÕES
NUVEMSHOP_CLIENT_ID = "22395"
NUVEMSHOP_CLIENT_SECRET = "d92860c7e62e4c3b129e32eac27d7844f4107eb7e787f553"
NUVEMSHOP_REDIRECT_URI = "https://autopost-nuvemshop.up.railway.app/oauth/callback"

FACEBOOK_PAGE_ID = "105809162380078"
FACEBOOK_ACCESS_TOKEN = (
    "EAA7sfnzxQ6QBPuLP7pBzg75e67zxSkLiBsOklZCpznDpFketMxVM4tJcikpHvgFMmMZBfOLATIJKhMIVruLRSzMQiqgIjhcLZBiyEawZAKDI4RJJ4zJNS28tJsis3TQZByEyHOFKi63RyI0SL4goKIyn9mvDZAZANnuWdEZAdFqEDmywNEyRPXPfe6Aq7jSJVAZDZD"
)

# 🔐 ROTA DE AUTORIZAÇÃO
@app.route("/auth")
def auth():
    return redirect(
        f"https://www.nuvemshop.com.br/apps/authorize?client_id={NUVEMSHOP_CLIENT_ID}&redirect_uri={NUVEMSHOP_REDIRECT_URI}&response_type=code"
    )

# 🔐 CALLBACK COM O CODE
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

