import pyodbc
from flask import Flask, redirect, url_for, render_template, request

def connectDB():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-0PSVL5P\MSQLSERVER1;"
        "Database=QLNV;"
        "Trusted_Connection=yes;"
    )
    return conn

def checkExistAccount(user_name, passwd):
    conn = connectDB()
    cursor = conn.cursor()
    # cursor.execute("SELECT username FROM thong_tin WHERE username=? and pass=?", user_name, passwd)
    cursor.execute("SELECT username FROM nhan_vien WHERE username= '" +user_name+ "' and pass= '" +passwd+ "'")
    for row in cursor:
        return row


def getAllInfor():
    users = []
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT ID, USERNAME, HOTEN, EMAIL, SDT
                        FROM NHAN_VIEN 
    """)
    for row in cursor:
        users.append({"ID": row[0], "username": row[1], "name": row[2], "email": row[3], "phone": row[4]})
    return users


def getOneRecord(user_name):
    user=[]
    conn = connectDB()
    cursor = conn.cursor()
    # cursor.execute("SELECT username FROM thong_tin WHERE username=? and pass=?", user_name, passwd)
    cursor.execute("""
    SELECT ID, USERNAME, HOTEN, EMAIL, SDT, TENPB, TENCV, CHUYENNGANH,  LUONGCB, HSL, LUONGCB*HSL AS LUONG
    FROM (NHAN_VIEN JOIN LUONG ON NHAN_VIEN.BacLuong=LUONG.BacLuong) JOIN PHONG_BAN ON NHAN_VIEN.MaPB=PHONG_BAN.MaPB 
																	JOIN CHUC_VU ON NHAN_VIEN.MaCV=CHUC_VU.MaCV
																	JOIN TRINH_DO_HOC_VAN ON TRINH_DO_HOC_VAN.MaTDHV=NHAN_VIEN.MaTDHV
    WHERE USERNAME= '""" +user_name+ """ '""")
    for row in cursor:
        user.append({"ID": row[0], "username": row[1], "name": row[2], "email": row[3], "phone": row[4], "phong": row[5], "chucvu": row[6], "chuyennganh": row[7], "luongcb": row[8], "hsl": row[9], "luong": row[10]})
    return user

def getUserByName(fullname):
    user=[]
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("select hoten, sdt from Nhan_vien where hoten like N'%" +fullname+ "%'")
    for row in cursor:
        print(1)
        user.append({ "name": row[0], "phone": row[1]})
    return user

app = Flask(__name__)
# ma hoa session cookie de tranh bi tan cong
# app.config["SECRET_KEY"] = "thuy1234"

@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        passwd = request.form["password"]
        rec=checkExistAccount(user_name, passwd)
        if rec:
            return redirect(url_for("welcome", name=user_name))
    return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        return redirect(url_for("login"))

@app.route("/user/<name>")
def welcome(name):
    if name=="admin":
        return render_template("actionAdmin.html", name=name)
    record=getOneRecord(name)
    return render_template("userInfo.html", name=name, record=record)
    # return str(record)

@app.route("/select/list")
def selectList():
    records=getAllInfor()
    return render_template("userList.html", records=records)

@app.route("/insert")
def insertUser():
    return f"<h2>Insert Completed!</h2>"

@app.route("/update")
def updateUser():
    return f"<h2>Update Completed!</h2>"


@app.route("/delete")
def delete():
    return f"<h2>Delete Completed!</h2>"


# @app.route("/find")
# def findtUser():
#     return f"<h2>Your worker's information is below!</h2>"

@app.route("/find", methods=['POST', 'GET'])
def findUser():
    if request.method == "POST": #loi pthuc khong phai Get ma la Post
        hoten = request.form["name"]
        records=getUserByName(hoten)
        if records:
            return render_template("infoFind.html", name=hoten, records=records)
    return f"<h1>Not found</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#attack: http://192.168.68.108:5000/user%3Fan1214