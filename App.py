from flask import Flask,render_template,request,jsonify
from TimeJob import search_times_jobs


app = Flask(__name__,template_folder="templates")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Results",methods=["post"])
def Searched():
    term = request.form.get("Term")
    return jsonify(search_times_jobs(term))




if __name__ == '__main__':
    app.run(debug=True)