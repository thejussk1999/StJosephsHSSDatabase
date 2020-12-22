from flask import *
from deletionboats import *
import pyodbc
app = Flask(__name__,template_folder='Templates')
app.config['SECRET_KEY'] = 'STJHSS'
conn=pyodbc.connect('Driver={SQL Server};'
                     'Server=DESKTOP-0UVKCDA;'
                     'Database=StJosephs;'
                     'Trusted_Connection=yes;');
cursor=conn.cursor()

@app.route('/reserveview')
def viewreserves():
	data=cursor.execute("SELECT * FROM Reserves");
	return render_template('reserveview.html',data=data)

@app.route('/deletionform',methods=['GET','POST'])
def stdelete():
    form=RDelete()
    studrolls=[]
    cursor.execute('SELECT * FROM Reserves')
    for row in cursor:
        studrolls.append(int(row[0]))
    if request.method=="POST":
        studentid=int(request.form.get('stid'))
        if(studentid in studrolls):
            cursor.execute("DELETE FROM Reserves WHERE RID=?",(studentid))
            return redirect(url_for("delsuccess"))
        else:
            return redirect(url_for("delfail"))
     
    return render_template('/deletionform.html',form=form)