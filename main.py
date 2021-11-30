from flask import *
from threading import Thread
from grabGrades import *

app = Flask('')
uname = ""
psw = ""
deeGrades = []

@app.route('/')
def home():
  return render_template("form.html")

@app.route('/results', methods = ['GET', 'POST'])
def results():
  if(request.method == "POST"):
    uname = request.form["uname"]
    psw = request.form["psw"]
    gettyGrades = grabGrades(uname, psw)
    if(gettyGrades.deGrades == []):
      return render_template("wrong.html")
    else:
      return render_template("results.html", leGrades = gettyGrades.deGrades, leName = gettyGrades.deName)
  else:
      return render_template("wrong.html")

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
