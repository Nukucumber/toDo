import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for
from data_module import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = getData()
    
    if request.method == "POST":
        if "add" in request.form:
            subject = request.form["subject"]
            task_name = request.form["task_name"]
            dateline = request.form["dateline"]
            description = request.form["description"]
            updateDate("ADD", data, subject, task_name, dateline, description)
            
            return redirect(url_for("index"))
        
        if "delete" in request.form:
            subject = request.form["subject"]
            task_name = request.form["task_name"]
            updateDate("DELETE", data, subject, task_name)

            return redirect(url_for("index"))


    return render_template("index.html", data = data)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000)