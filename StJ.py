from flask import *
from stlogin import LoginPage
from studentry import StudentEntry
from studelete import StudentDelete
from studlogin import StudentLog
from marksupdate import UpdateMarks
import pyodbc


conn=pyodbc.connect('Driver={SQL Server};'
                     'Server=DESKTOP-0UVKCDA;'
                     'Database=StJosephs;'
                     'Trusted_Connection=yes;');
cursor=conn.cursor()

app = Flask(__name__,template_folder='Templates')
app.config['SECRET_KEY'] = 'STJHSS'


@app.route('/')
def homepage():
    return render_template('/homepage.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form=LoginPage()
    user=request.form.get('userid')
    pwd=request.form.get('passw')
    if request.method=='POST':
        pass
        if(user=='Thejus' and pwd=='principal'):
            name=user
            return redirect(url_for("admin"))
        else:
            return render_template('/entryfailure.html')
    return render_template('signup.html',form=form)

@app.route('/studentadmission',methods=['GET','POST'])
def studentry():
    form=StudentEntry()
    if request.method=="POST":
        studentid=request.form.get('stid')
        studentname=request.form.get('stdname')
        studentphone=request.form.get('phone')
        studentclass=request.form.get('secclass')
        studentfather=request.form.get('father')
        studentmother=request.form.get('mother')
        studentaddress=request.form.get('address')
        try:
            data=(int(studentid),studentname,studentclass,int(studentphone),studentfather,studentmother,studentaddress)
            cursor.execute("INSERT INTO Student VALUES(?,?,?,?,?,?,?)",data)
        except:
            return redirect(url_for("efailure"))
        else:
            return redirect(url_for("esuccess"))
    return render_template('studentadmission.html',form=form)

@app.route('/entrysuccess')
def esuccess():
    return render_template('/entrysuccess.html')
    
@app.route('/entryfailure')
def efailure():
    return render_template('/entryfailure.html')

@app.route('/adminhpage')
def admin():
    data=[]
    
    sql="SELECT * FROM Student"
    cursor.execute(sql)
    data.append(cursor.fetchall())
    
    sql= 'SELECT TOP 3 * FROM (SELECT Student_ID,AVG(Marks) AS MarksAgg FROM Examination GROUP BY Student_ID) A ORDER BY MarksAgg DESC;'
    cursor.execute(sql)
    data.append(cursor.fetchall())
    
    sql="SELECT Subject_ID,AVG(Marks) AS MarksAgg FROM Examination GROUP BY Subject_ID ORDER BY MarksAgg DESC;"
    cursor.execute(sql)
    data.append(cursor.fetchall())
    
    sql='SELECT Degree,COUNT(*) AS FacultyCount FROM StudDegree GROUP BY Degree ORDER BY FacultyCount DESC'
    cursor.execute(sql)
    v=cursor.fetchall()
    data.append(v)
    
    name="Principal"
    return render_template('adminhpage.html',data=data,name=name)
    
@app.route('/deletesuccess')
def delsuccess():
    return render_template('/deletesuccess.html')

@app.route('/deletefailure')
def delfail():
    return render_template('/deletefailure.html')
    
@app.route('/deletestudent',methods=['GET','POST'])
def stdelete():
    form=StudentDelete()
    studrolls=[]
    cursor.execute('SELECT * FROM Student')
    for row in cursor:
        studrolls.append(int(row[0]))
    if request.method=="POST":
        studentid=int(request.form.get('stid'))
        if(studentid in studrolls):
            cursor.execute("DELETE FROM Student WHERE StudentID=?",(studentid))
            return redirect(url_for("delsuccess"))
        else:
            return redirect(url_for("delfail"))
     
    return render_template('/deletestudent.html',form=form)   

@app.route('/studentloginentry',methods=['GET','POST'])
def studloginp():
    form=StudentLog()
    studrolls=[]
    cursor.execute('SELECT * FROM Student')
    for row in cursor:
        studrolls.append(int(row[0]))
    if request.method=="POST":
        studentid=int(request.form.get('stid'))
        if(studentid in studrolls):
            return redirect(url_for("stloginhpage",id=studentid))
    return render_template('/studentloginentry.html',form=form)

@app.route('/stloginhome')
def stloginhpage():
    data=[]
    studid=request.args.get('id',None)
    cursor.execute("SELECT * FROM Student WHERE StudentID=?",studid)
    personal=cursor.fetchall()
    data.append(personal)
    
    cursor.execute("SELECT Subject_ID,Marks FROM Examination WHERE Student_ID=?",(studid))
    exam=cursor.fetchall()
    data.append(exam)
    
    cursor.execute("SELECT * FROM StudAttend WHERE Student_ID=?",(studid))
    exam=cursor.fetchall()
    data.append(exam)
    
    cursor.execute("SELECT DISTINCT Extra_ID FROM DimExtra_Curricular WHERE Student_ID=?",(studid))
    exam=cursor.fetchall()
    data.append(exam)
    return render_template('stloginhome.html',value=studid,data=data)
    
@app.route('/updatemarks',methods=['GET','POST'])
def marksup():
    form=UpdateMarks()
    studrolls=[]
    cursor.execute('SELECT * FROM Student')
    for row in cursor:
        studrolls.append(int(row[0]))
    if request.method=="POST":
        userid=int(request.form.get('stid'))
        if userid in studrolls:
            subjid=request.form.get('subid')
            marks=int(request.form.get('marks'))
            cursor.execute("SELECT Marks FROM Examination WHERE Student_ID=? AND Subject_ID=?",(userid,subjid))
            marksold=int(cursor.fetchall()[0][0])
            if(marksold<marks):
                cursor.execute("UPDATE Examination SET Marks=? WHERE Student_ID=? AND Subject_ID=?",(marks,userid,subjid))
        else:
            return render_template('/entryfailure.html',form=form)
    return render_template('/updatemarks.html',form=form)

