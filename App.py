from flask import Flask,render_template,request,jsonify
from TimeJob import SearchTimesJobs
import asyncio


app = Flask(__name__,template_folder="templates")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Results",methods=["post"])
def Searched():
    term = request.form.get("Term")
    return jsonify(asyncio.run(SearchTimesJobs(term)))




if __name__ == '__main__':
    app.run(debug=True)