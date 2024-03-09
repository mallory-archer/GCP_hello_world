# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route("/")
# def hello_world():
#     return "Hello World!"
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        user_input = request.form["user_input"]
        return render_template("index.html", message=f"You entered: {user_input}")
    else:
        return render_template("index.html", message="")

if __name__ == "__main__":
    app.run(debug=True)
