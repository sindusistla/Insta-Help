from flask import Flask,render_template,request, json

# create a app
app=Flask(__name__)

# Basic route
@app.route("/")
def main():
    return render_template('HomePage.html')

if __name__ == "__main__":
	app.run()
