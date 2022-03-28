from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import datetime
import re



app = Flask(__name__)
cors = CORS(app)
app.config['MYSQL_HOST'] = '139.59.249.192'
app.config['MYSQL_USER'] = 'farmer'
app.config['MYSQL_PASSWORD'] = '9517538426Gp'
app.config['MYSQL_DB'] = 'FARMS'
mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/create/<string:user_id>/<string:farm_name>')
def create_farm(user_id,farm_name):  
    cur = mysql.connection.cursor() 
    cur.execute("INSERT INTO farm (user_id) VALUES (%s)", [user_id])
    cur.execute(""" SELECT farm_id FROM farm WHERE user_id = %s ORDER BY farm_id DESC LIMIT 1 """, [user_id] )
    data = cur.fetchall()
    farm_id = data[0]
    temp = 0
    humid = 0
    cur.execute(""" UPDATE farm SET farm_name=%s WHERE farm_id = %s """, (farm_name, farm_id) )
    for i in range(5) :
        cur.execute("""INSERT INTO farm_details (farm_id,temp,humid) VALUES (%s, %s, %s)""", (farm_id, temp, humid))
    mysql.connection.commit()
    cur.close() 
    return "Created!"

@app.route('/register/<string:username>/<string:password>') #register
def register(username,password,):
    password = bcrypt.generate_password_hash(password)
    cur = mysql.connection.cursor() 
    cur.execute("""INSERT INTO users (username,password) VALUES (%s, %s)""", [username, password])
    mysql.connection.commit()
    cur.close()
    return "Registered"

@app.route('/login/<string:username>/<string:password>') #login
def login(username,password,):
    check_password = None
    user_data = []
    cur = mysql.connection.cursor() 
    cur.execute(""" SELECT user_id,username,password FROM users WHERE username = %s  """, [username] )
    data = cur.fetchall()
    if data :
        encPassword = data[0][2]
        check_password = bcrypt.check_password_hash(encPassword, password)
        if check_password == True :  
            data = data[0][0] , data[0][1]
            user_data.append({"user_id":data[0],"username":data[1],"status":200})
        else:
            user_data.append({"status":404})
    else :
        user_data.append({"status":404})
        pass
    mysql.connection.commit()
    cur.close() 
    return jsonify(user_data)

    

@app.route('/sent/<string:farm_id>/<string:temp>/<string:humid>') #บอร์ดส่งข้อมูลมา #serverจัดการข้อมูล
def sent(farm_id,temp,humid):
    temp = float(temp)
    humid = int(humid)
    farm_id == str(farm_id)
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO farm_details (farm_id,temp,humid) VALUES (%s, %s, %s)""", [farm_id, temp, humid])
    tempdata = []
    humiddata = []
    time_now = datetime.datetime.now()
    time = time_now - datetime.timedelta(seconds=10)
    cur.execute(""" SELECT temp,humid FROM farm_details WHERE farm_id = %s and datetime > %s ORDER BY id DESC """, [farm_id, time] )
    raw_data = cur.fetchall()
    for i in range(len(raw_data)) :
        tempdata.append(raw_data[i][0])
        humiddata.append(raw_data[i][1])
    tempdata = max(tempdata)
    humiddata = max(humiddata)
    cur.execute(""" UPDATE farm SET temp=%s, humid=%s, time=%s WHERE farm_id = %s """, (tempdata, humiddata, time_now, farm_id) )
    mysql.connection.commit()
    cur.close() 
    return "Sent!"  

@app.route('/read/<string:user_id>') #มือถืออ่านข้อมูล
def get_all_farm(user_id):
    data = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farm WHERE user_id = %s", (user_id,))
    raw_data = cur.fetchall()
    cur.close()
    for cur in raw_data:
        data.append({"user_id":cur[0],"farm_id":cur[1],"farm_name":cur[2],"temp":cur[3],"humid":cur[4],"time":str(cur[5]),"fan_status":cur[6]
        ,"fog_status":cur[7],"Automate":cur[8],"fix_temp":cur[9],"fix_humid":cur[10]})
    return jsonify(data)

@app.route('/read/farm/<string:farm_id>') #มือถืออ่านข้อมูลแต่ละหน้า
def get_one_farm(farm_id):
    data = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farm WHERE farm_id = %s", [farm_id])
    raw_data = cur.fetchall()
    cur.close()
    for cur in raw_data:
        data.append({"user_id":cur[0],"farm_id":cur[1],"farm_name":cur[2],"temp":cur[3],"humid":cur[4],"time":str(cur[5]),"fan_status":cur[6]
        ,"fog_status":cur[7],"Automate":cur[8],"fix_temp":cur[9],"fix_humid":cur[10]})
    return jsonify(data)

@app.route('/change-option/<string:farm_id>/<string:Automate>/<string:fix_temp>/<string:fix_humid>/<string:fan_status>/<string:fog_status>') #ตั้งค่าต่างๆฟาร์ม from Mobile
def change_option(farm_id,Automate,fix_temp,fix_humid,fan_status,fog_status):
    cur = mysql.connection.cursor()
    cur.execute(""" UPDATE farm SET Automate=%s,fix_temp = %s,fix_humid = %s,fan_status = %s,fog_status = %s WHERE farm_id = %s """, (Automate,fix_temp,fix_humid,fan_status,fog_status, farm_id) )
    mysql.connection.commit()
    cur.close()
    return "Success!" 

@app.route('/check-iot/<string:farm_id>') #เช็คสถานะiot
def check_iot(farm_id): 
    cur = mysql.connection.cursor()
    cur.execute("SELECT fan_status,fog_status FROM farm WHERE farm_id = %s", (farm_id,))
    raw_data = cur.fetchall()
    cur.close()
    raw_data = re.subn('[(())]','',str(raw_data))[0]
    return str(raw_data)

@app.route('/check-condition/<string:farm_id>/<string:fan_status>/<string:fog_status>') #เปลี่ยนสภาวะ
def check_contidion(farm_id,fan_status,fog_status): 
    cur = mysql.connection.cursor()
    cur.execute("SELECT temp,humid,fix_temp,fix_humid,Automate,fan_status,fog_status FROM farm WHERE farm_id = %s", (farm_id,))
    raw_data = cur.fetchall()
    temp = raw_data[0][0]
    humid = raw_data[0][1]
    fix_temp = raw_data[0][2]
    fix_humid = raw_data[0][3]
    Automate = raw_data[0][4]
    fan_status = raw_data[0][5]
    fog_status = raw_data[0][6]
    if Automate == 1 :
        if temp > fix_temp :
            fan_status = 1
        else :
            fan_status = 0
        if humid < fix_humid : 
            fog_status = 1
        else :
            fog_status = 0
    elif Automate == 0 :
        fog_status = fog_status
        fan_status = fan_status
    else :
        return ("Error")
    cur.execute(""" UPDATE farm SET fan_status = %s, fog_status = %s WHERE farm_id = %s """, (fan_status,fog_status,farm_id,) )
    mysql.connection.commit()
    cur.close()
    return ""

@app.route('/statistic/<string:farm_id>') 
def statistic(farm_id):
    tempdata = []
    humiddata = []
    cur = mysql.connection.cursor()
    cur.execute(""" SELECT temp,humid FROM farm_details WHERE farm_id = %s ORDER BY id DESC LIMIT 1 """, [farm_id] )
    raw_data = cur.fetchall()
    tempdata.append(raw_data[0][0])
    humiddata.append(raw_data[0][1])
    time = datetime.datetime.now()
    cur.execute("""INSERT INTO statistic (farm_id,temp,humid,time) VALUES (%s, %s, %s, %s)""", (farm_id, tempdata, humiddata, time))
    mysql.connection.commit()
    cur.close() 
    return "Sent!" 

if __name__ == "__main__":
    app.run(debug=True)