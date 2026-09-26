"""ColorBurst — a colorful Flask webapp, ready for deployment."""

from flask import Flask, render_template, request, redirect, url_for, flash
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-in-production"

# Prometheus metrics
metrics = PrometheusMetrics(app)

# ------------------------------------------------------------------
# Demo "database" — replace with real DB (PostgreSQL / SQLite) later
# ------------------------------------------------------------------
MESSAGES = []
VISITOR_COUNT = 0


@app.before_request
def count_visitor():
    global VISITOR_COUNT
    VISITOR_COUNT += 1


@app.context_processor
def inject_globals():
    return {"visitor_count": VISITOR_COUNT}


@app.route("/")
def home():
    return render_template("index.html", active="home")


@app.route("/features")
def features():
    return render_template("features.html", active="features")


@app.route("/about")
def about():
    return render_template("about.html", active="about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("⚠️ Please fill in all fields.", "error")
        elif "@" not in email:
            flash("⚠️ Please enter a valid email address.", "error")
        else:
            MESSAGES.append({
                "name": name,
                "email": email,
                "message": message
            })

            flash(
                f"🎉 Thanks {name}! Your message has been received.",
                "success"
            )

            return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        active="contact",
        messages=MESSAGES
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
