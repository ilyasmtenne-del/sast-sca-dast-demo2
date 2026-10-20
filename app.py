import re
from flask import Flask, request, abort
from markupsafe import escape
from werkzeug.serving import WSGIRequestHandler

# Masque la version dans l'en-tête "Server"
WSGIRequestHandler.version_string = lambda self: "webserver"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024

NAME_PATTERN = re.compile(r"^[\w\s\-]{1,100}$")

PAGE = (
    "<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
    "<title>{title}</title></head><body>{body}</body></html>"
)


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; frame-ancestors 'none'; "
        "form-action 'none'; base-uri 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return PAGE.format(
        title="Flask DAST demo",
        body="<h1>Flask DAST demo</h1><a href='/hello?name=test'>hello</a>",
    )


@app.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "world")
    if not NAME_PATTERN.match(name):
        abort(400)
    return PAGE.format(title="Hello", body=f"<h1>Hello {escape(name)}</h1>")


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
def handle_error(e):
    return PAGE.format(title="Erreur", body="<p>Requête invalide.</p>"), e.code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
