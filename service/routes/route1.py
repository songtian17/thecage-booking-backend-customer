from service import app


@app.route("/route1/")
def route1():
    return "Hello Route 1"
