import pyodbc
from flask import Flask, redirect, url_for, render_template, request
from requests import get
import hashlib

def connectDB():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-0PSVL5P\MSQLSERVER1;"
        "Database=QLNV;"
        "Trusted_Connection=yes;"
    )
    return conn

app = Flask(__name__)
# ma hoa session cookie de tranh bi tan cong
# app.config["SECRET_KEY"] = "thuy1234"

@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        passwd = request.form["password"]
        # passwd=hashlib.md5(passwd.encode('utf-8')).hexdigest()
        passwd=hashlib.sha1(passwd.encode('utf-8')).hexdigest()
        print(passwd) 
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nhan_vien WHERE username= ? and pass= ?", (user_name, passwd))
        # cursor.execute("SELECT * FROM nhan_vien WHERE username= '" +user_name+ "' and pass= '" +passwd+ " '")
        data=cursor.fetchone()
        if data:
            return redirect(url_for("welcome", name=user_name))
    return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        return redirect(url_for("login"))

@app.route("/user/<name>")
def welcome(name):
    # name=name.strip('\'')
    if name=="asadmin":
        return render_template("actionAdmin.html", name=name)
    conn = connectDB()
    cursor = conn.cursor()
    # cursor.execute("SELECT username FROM thong_tin WHERE username=? and pass=?", user_name, passwd)
    cursor.execute("""
    SELECT ID, USERNAME, HOTEN, EMAIL, SDT, TENPB, TENCV, CHUYENNGANH,  LUONGCB, HSL, LUONGCB*HSL AS LUONG
    FROM (NHAN_VIEN JOIN LUONG ON NHAN_VIEN.BacLuong=LUONG.BacLuong) JOIN PHONG_BAN ON NHAN_VIEN.MaPB=PHONG_BAN.MaPB 
																	JOIN CHUC_VU ON NHAN_VIEN.MaCV=CHUC_VU.MaCV
																	JOIN TRINH_DO_HOC_VAN ON TRINH_DO_HOC_VAN.MaTDHV=NHAN_VIEN.MaTDHV
    WHERE USERNAME= ?""", name)
    # cursor.execute("""
    # SELECT ID, USERNAME, HOTEN, EMAIL, SDT, TENPB, TENCV, CHUYENNGANH,  LUONGCB, HSL, LUONGCB*HSL AS LUONG
    # FROM (NHAN_VIEN JOIN LUONG ON NHAN_VIEN.BacLuong=LUONG.BacLuong) JOIN PHONG_BAN ON NHAN_VIEN.MaPB=PHONG_BAN.MaPB 
	# 																JOIN CHUC_VU ON NHAN_VIEN.MaCV=CHUC_VU.MaCV
	# 																JOIN TRINH_DO_HOC_VAN ON TRINH_DO_HOC_VAN.MaTDHV=NHAN_VIEN.MaTDHV
    # WHERE USERNAME= '""" +name+ """ '""")
    rec= cursor.fetchone()
    if rec:
        return render_template("userInfo.html", rec=rec, name=name)
    else:
        return f"<h1>Not found</h1>"


@app.route("/userList.html")
def selectList():
    user=[]
    conn = connectDB()
    cursor = conn.cursor()
    # cursor.execute("SELECT username FROM thong_tin WHERE username=? and pass=?", user_name, passwd)
    cursor.execute("""
    SELECT ID, USERNAME, HOTEN, EMAIL, SDT, TENPB, TENCV, CHUYENNGANH,  LUONGCB, HSL, LUONGCB*HSL AS LUONG
    FROM (NHAN_VIEN JOIN LUONG ON NHAN_VIEN.BacLuong=LUONG.BacLuong) JOIN PHONG_BAN ON NHAN_VIEN.MaPB=PHONG_BAN.MaPB 
																	JOIN CHUC_VU ON NHAN_VIEN.MaCV=CHUC_VU.MaCV
																	JOIN TRINH_DO_HOC_VAN ON TRINH_DO_HOC_VAN.MaTDHV=NHAN_VIEN.MaTDHV
    """)
    for row in cursor:
        user.append({"ID": row[0], "username": row[1], "name": row[2], "email": row[3], "phone": row[4], "phong": row[5], "chucvu": row[6], "chuyennganh": row[7], "luongcb": row[8], "hsl": row[9], "luong": row[10]})
    return render_template("userList.html", rec=user)

@app.route("/insert")
def insertUser():
    return f"<h2>Insert Completed!</h2>"

@app.route("/update")
def updateUser():
    return f"<h2>Update Completed!</h2>"


@app.route("/delete")
def delete():
    return f"<h2>Delete Completed!</h2>"

@app.route("/resetPass")
def reset():
    return f"<h2>Password of Worker Reseted Completely!</h2>"

# @app.route("/find")
# def findtUser():
#     return f"<h2>Your worker's information is below!</h2>"

@app.route("/find", methods=['POST', 'GET'])
def findUser():
    if request.method == "POST": #loi pthuc khong phai Get ma la Post
        hoten = request.form["name"]
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("select hoten, sdt from Nhan_vien where hoten like N'%" +hoten+ "%'")
        if cursor:
            return render_template("infoFind.html", name=hoten, rec=cursor)
    return f"<h1>Not found</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#attack: http://192.168.68.108:5000/user%3Fan1214