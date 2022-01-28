# Labraries for flask , image upload -----------------
from flask import Flask,  flash, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import urllib.request
import os
from werkzeug.utils import secure_filename
import json
import requests

# libraries for ZTECO K40 -------------------
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK, const
import zk
print (zk.__file__)
conn = None



# ------------------------------------


UPLOAD_FOLDER = 'static/uploads/'


# SQL Database connection ------------------------
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biometrics'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



# folder upload allowed format --------------------
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# function for enrolling student in the database and the device ------------------
@app.route('/uploading', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #insering into database table 
        studentname = request.form['studentname']
        admissionnumber = request.form['admissionnumber']
        admissionnumber1 = request.form['admissionnumber1']  
        classgroup = request.form['classgroup']
        age = request.form['age']
        gender = request.form['gender']
        parentname = request.form['parentname']
        parentnumber = request.form['parentnumber']
        userfingerprintid = int(admissionnumber)

        # connecting to ZKTeco device ---------------
        zk = ZK('192.168.1.203', port=4370, verbose=True)
        conn = zk.connect()
        # inserting into the device 
        conn.set_user(uid=userfingerprintid, name='{}'.format(studentname), privilege=const.USER_DEFAULT, password='', user_id='{}'.format(userfingerprintid))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (studentname, admissionnumber , admissionnumber1 , classgroup , age , gender, parentname , parentnumber , imagename) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)",
                    (studentname, admissionnumber , admissionnumber1, classgroup, age, gender, parentname  , parentnumber , filename ))
        mysql.connection.commit()

           

         
        flash('Student Successfully Added with a Fingerprint')
        return render_template('successfullyadded.html' , addmission= userfingerprintid )
    else:
        print ("Process terminated with an Error")
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


 
    
# Live capture code ---------------------------------------------
@app.route('/livecapturingdata')
def livecapturingdata():
    zk = ZK('192.168.1.203', port=4370)
    conn = zk.connect()
     
    for attendance in conn.live_capture():
        if attendance is None:
            print('no attendance')
        else:
            print (attendance)
            templateing = attendance
            saa = 'Successfully'
            cur1 = mysql.connection.cursor()

            fingerprintid = attendance.user_id

            cur1.execute("INSERT INTO studentattendance (template , time, fingerprintid ) VALUES (%s, %s , %s)",
                        (templateing, saa , fingerprintid  ))
            mysql.connection.commit()


            cursor = mysql.connection.cursor()
            sql_select_query = """select * from students where admissionnumber = %s"""
            # set variable in query
            cursor.execute(sql_select_query, (fingerprintid,))
            # fetch result
            record = cursor.fetchall()

            timeofpassing = str(templateing)

            for x in record:

                print(x['parentnumber'])
                
                url="URL_API_KEY"
                headers={'Content-type':'application/json','Accept':'application/json'}
                data={
                    "userid": "Username",
                    "password" : "Password",
                    "senderid": "Notify_MSG",
                    "msgType": "text",
                    "duplicatecheck": "true",
                    "sms": [
                            {
                            "mobile": [x['parentnumber']],
                            "msg":  "Dear Parent/Guardian,  "+ x['studentname']+" Admno :  " + str(x['admissionnumber1']) +" has passed through the Gate,  FingerPrint No : "+ timeofpassing[13:]
                            }
                    ]
                }
                r=requests.post(url,data=json.dumps(data),headers=headers)
                response = json.loads(r.content)
                print(response)

                 
               
            

            
            
    return render_template("dashboard.html")

@app.route('/studentsingle', methods=['POST'])
def studentsingle():
    
    studentid = request.form['studentid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s ", (studentid))
    data = cur.fetchall()
  
    from_db = []
    for x in  data:
        fingerprintid = x['admissionnumber']
        from_db.append(x['admissionnumber'])

   
    print(from_db)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM studentattendance WHERE fingerprintid = %s ORDER BY template DESC;  ", (from_db))
    data1 = cur.fetchall()

    return render_template("studentsingle.html" , singlestudent = data , pic = data , studenttemplate=data1   )   

  
@app.route('/deletestudent', methods=['POST'])
def deletestudent():
    
    studentid = request.form['studentid']
    print(studentid)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s ; ", (studentid))
    mysql.connection.commit()


    flash('Student Deleted Successfully')
    return render_template('delete_successfully.html')





@app.route('/class_single')
def class_single():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE classgroup LIKE 'form1' ")
    data = cur.fetchall()
    cur.close()
    return render_template("class_single.html" , classgroup = data)


@app.route('/class_single1')
def class_single1():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE classgroup LIKE 'form2' ")
    data = cur.fetchall()
    cur.close()
    return render_template("class_single.html" , classgroup = data)


@app.route('/class_single2')
def class_single2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE classgroup LIKE 'form3' ")
    data = cur.fetchall()
    cur.close()
    return render_template("class_single.html" , classgroup = data)


@app.route('/class_single3')
def class_single3():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE classgroup LIKE 'form4' ")
    data = cur.fetchall()
    cur.close()
    return render_template("class_single.html" , classgroup = data)


@app.route('/classes')
def classes():
    return render_template("class.html")     

@app.route('/')
def home():
    return render_template("firstpage.html")

# Signup page -------------------------------------------------------
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        fullnames = request.form['fullnames']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        uname = request.form['uname']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO administrators (full_names, phonenumber , email , username , password) VALUES (%s, %s,%s,%s,%s)",
                    (fullnames, phonenumber, email, uname, hash_password))
        mysql.connection.commit()
        session['full_names'] = fullnames
        session['email'] = email
        session['phonenumber'] = phonenumber
        session['username'] = uname
        return redirect(url_for("dashboard"))

# login validation of a user ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM administrators WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['full_names'] = user['full_names']
                session['email'] = user['email']
                session['username'] = user['username']
                session['phonenumber'] = user['phonenumber']
                return render_template("dashboard.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("firstpage.html")

        

# Dasbhoard -------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# Logout ---------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return render_template("firstpage.html")

 

if __name__ == '__main__':
    app.secret_key = "shicenzi5477!@aa"
    app.run(debug=True)
