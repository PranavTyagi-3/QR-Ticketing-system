from flask import Flask,render_template,request, jsonify, session, redirect, url_for, send_file
import sqlite3
import os
import pandas as pd

app=Flask(__name__)
app.config['DATABASE'] = 'AutoQR.db'
app.secret_key = 'TH15_1S_@_S3CR3T_K3Y'

UPLOAD_FOLDER = "static/Uploads"
ATTENDANCE_LIST = "static/Attendance"

@app.route('/home',methods=("GET","POST"))
def home():
    if request.method=="POST":
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        passwd = request.form['password']
        username = request.form['Club Name']
        
@app.route('/login',methods=("GET","POST"))
def login():
    if request.method=="POST":
        login_id=request.form['username']
        passwd = request.form['password']
        login_conn = sqlite3.connect(app.config['DATABASE'])
        cur=login_conn.cursor()
        cur.execute('SELECT password,code FROM users WHERE username = ?', (login_id,))
        result = cur.fetchone()
        login_conn.close()
        print("1")
        if result and result[0] == passwd:
            print(result)
            session['login_id'] = request.form['username']
            session['scanner_code'] = result[1]
            return redirect(url_for('admin'))
        else:
            print("Wrong")
            return render_template('login.html',message="Wrong Id or Password")

    return render_template('login.html')

@app.route('/admin.html',methods=("GET","POST"))
def admin():
    if 'login_id' not in session:
        return 'Access denied. Please log in first.'
        
    if request.method=="POST":
        if 'participantsFile' not in request.files:
            return "No file part"
        try:
            file = request.files['participantsFile']   
        except:
            return render_template('admin.html',message="No valid file uploaded")
        
        allowed_extensions = {'xlsx'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('admin.html',message="Invalid File Type")  
        
        file.save(os.path.join(UPLOAD_FOLDER, session['login_id']+'.xlsx'))
        add_conn = sqlite3.connect(app.config['DATABASE'])
        cur=add_conn.cursor()
        li=func(os.path.join(UPLOAD_FOLDER, session['login_id']+'.xlsx'))    # A list having nested tuples for each row values
        sql=f"insert or ignore into {session['login_id']}T (name,reg,mail) VALUES (?,?,?)"
        cur.executemany(sql, li)
        add_conn.commit()
        add_conn.close()
    
    login_id = session['login_id']
    scanner_code = session['scanner_code']
    table_name = login_id+"T"
    new_conn = sqlite3.connect(app.config['DATABASE'])
    cur=new_conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    temp=[i[0] for i in cur.fetchall()]
    table_exists = table_name in temp
    if table_exists:
        try:
            sql=f"SELECT COUNT(*) from {table_name}"
            row_count = cur.execute(sql).fetchone()[0]
            
        except:
            row_count=0
    else:
        row_count = 0
        sql=f"CREATE TABLE {table_name}(reg TEXT PRIMARY KEY, name TEXT, Attended TEXT DEFAULT 'False', Time TEXT,mail TEXT)"
        cur.execute(sql)
        new_conn.commit()
    new_conn.close()
    
    scanner_url = f"{request.url_root}scanner/{scanner_code}"
    print(scanner_url)
    return render_template('admin.html',code=scanner_code,count=row_count,event=login_id, scanner_url=scanner_url)

@app.route('/scanner/<scanner_code>',methods=["GET","POST"])
def scanner(scanner_code):
    check_conn = sqlite3.connect(app.config['DATABASE'])
    curr = check_conn.cursor()
    curr.execute("select * from users where code=?;",(scanner_code,))
    rec=curr.fetchone()
    if rec is not None:
        return render_template('index.html',id=rec[0])
    else:
        return "Incorrect Scanner Code, Please check the code"

@app.route('/process_data', methods=['POST'])
def process_qr():
    qr_data = request.json
    print("Received QR code data:", qr_data['data'])
    # You can process the data further here
    reg_n=qr_data['data'].upper()
    table_name=qr_data['table']
    time=qr_data['time']
    scan_conn = sqlite3.connect(app.config['DATABASE'],isolation_level='IMMEDIATE')
    sc_cur = scan_conn.cursor()
    sql=f"select reg from {table_name}"
    sc_cur.execute(sql)
    li=[i[0] for i in sc_cur.fetchall()]
    print(li)
    if reg_n in li:
        print("ACCEPTED", reg_n)
        result_message="Accepted"
        sql=f"UPDATE {table_name} set Attended='True', Time=? where reg=?"
        sc_cur.execute(sql,(time,reg_n))
        scan_conn.commit()
    else:
        print("REJECTED")
        result_message="Rejected"

    response_data = {'message': result_message}
    return jsonify(response_data)

@app.route('/download')
def download():
    if 'login_id' not in session:
        return 'Access denied. Please log in first.'
    login_id = session['login_id']
    conn = sqlite3.connect(app.config['DATABASE'])
    curr = conn.cursor()
    table_name=login_id+"T"
    
    sql=f"SELECT name,reg from {table_name} where Attended='True'"
    curr.execute(sql)
    rec=curr.fetchall()
    print(rec)
    df=pd.DataFrame(rec, columns=["Name","Registration Number"])
    file_path=os.path.join(ATTENDANCE_LIST, session['login_id']+'.xlsx')
    df.to_excel(file_path, index=False)
    print("Attendence List Generated")
    return send_file(file_path, as_attachment=True, download_name=session['login_id']+'.xlsx')

def func(path):
    excel_file_path = path
    df = pd.read_excel(excel_file_path)
    column_names = ['NAME', 'REGISTRATION NUMBER', 'Email Address']
    filtered_df = df[column_names]
    data_list = [tuple(row) for row in filtered_df.values]
    return data_list

@app.route('/super_admin_FN20983HRA')
def super_admin():
    pass
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')