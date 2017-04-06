#!python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/birthdays")
def birthdays():
	dates = {"Julian": 25, "Bob": 26, "Dan": 47, "Cornelius": 3}
	return render_template("birthdays.html", dates=dates)
	
if __name__ == "__main__":
	app.run()
