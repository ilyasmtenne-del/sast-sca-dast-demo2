from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Flask DAST demo</h1><a href='/hello?name=test'>hello</a>"

# Volontairement vulnérable (XSS réfléchi) pour que ZAP ait quelque chose à trouver
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
