from service import app


@app.route("/route2/")
def route2():
    return "Hello Route 2!"
