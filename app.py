import os
from flask import Flask
from flask import render_template
from flask import session,request, redirect
from flask import g
import sqlite3
import json 

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect("heartdb.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/")
def LoadIndex():
    return render_template('Index.html')

@app.route("/Home.html")
def LoadHome():
    return render_template('Home.html')

@app.route("/Main.html")
def LoadMain():
    return render_template('Main.html')

@app.route("/AdminLogin.html")
def LoadAdminLogin():
    return render_template('AdminLogin.html')

@app.route('/AdminLoginPost.html', methods = ['POST'])
def userloginpost():
    txtemail = request.form['username']
    txtpwd = request.form['username']
    if ((txtemail == "Admin") and (txtpwd == "Admin")):
        return render_template('upload.html')
    else:
        return render_template('AdminLogin.html', msg="Invalid User")

@app.route("/upload.html")
def Loadupload():
    return render_template('upload.html')

@app.route("/uploadsave.html", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':            
            photo.save(os.path.join(f'static/uploadfiles', photo.filename))
    
    import pandas
    df = pandas.read_csv('D:/StudentsProjects/HeartDisease/static/uploadfiles/'+photo.filename)
    print(df.to_html())

    conn = sqlite3.connect('heartdb.db')  

    df.to_sql('HeartAnalysisData', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 


    return render_template('upload.html',tables=df.to_html())

@app.route("/chart.html")
def Loadchart():
    return render_template('chart.html')

@app.route("/analysis.html")
def Loadanalysis():
    return render_template('analysis.html')

@app.route("/Negative.html")
def LoadNegative():
    return render_template('Negative.html')

@app.route("/Positive.html")
def LoadPositive():
    return render_template('Positive.html')

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)     
