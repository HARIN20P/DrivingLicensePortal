
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

applications = []
next_id = 1001


@app.route("/", methods=["GET", "POST"])
def index():
    global next_id

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dob = request.form.get("dob", "").strip()
        email = request.form.get("email", "").strip()
        license_type = request.form.get("license_type", "").strip()

        if name and dob and email and license_type:
            applications.append({
                "id": next_id,
                "name": name,
                "dob": dob,
                "email": email,
                "license_type": license_type,
                "status": "Submitted"
            })
            next_id += 1

        return redirect(url_for("index"))

    search = request.args.get("search", "").strip().lower()

    filtered = [
        a for a in applications
        if search in str(a["id"]).lower()
        or search in a["name"].lower()
        or search in a["status"].lower()
    ]

    return render_template(
        "index.html",
        applications=filtered,
        search=search
    )


@app.route("/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    global applications
    applications = [
        a for a in applications if a["id"] != application_id
    ]
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
