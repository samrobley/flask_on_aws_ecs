from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # you need host='0.0.0.0' to run on docker container
    app.run(debug=True, host='0.0.0.0')