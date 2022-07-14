from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['MYSQL_HOST'] = '139.59.249.192'
app.config['MYSQL_USER'] = 'farmer'
app.config['MYSQL_PASSWORD'] = '9517538426Gp'
app.config['MYSQL_DB'] = 'FARMS'
mysql = MySQL(app)
bcrypt = Bcrypt(app)



@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/createfarm/<string:user_id>/<string:farm_name>')
def create_farm(user_id,farm_name):  
    cur = mysql.connection.cursor() 
    cur.execute("INSERT INTO farm (user_id,farm_name) VALUES (%s, %s)", [user_id,farm_name])
    mysql.connection.commit()
    cur.close() 
    return "Created!"

@app.route('/delfarm/<string:farm_id>')
def delete_farm(farm_id):  
    cur = mysql.connection.cursor() 
    cur.execute("DELETE FROM farm WHERE farm_id = %s ", [farm_id])
    mysql.connection.commit()
    cur.close() 
    return "Deleted!"

@app.route('/alluser')
def alluser():  
    cur = mysql.connection.cursor() 
    cur.execute("SELECT username,user_id FROM users")
    raw_data = cur.fetchall()
    cur.close()
    data = []
    for cur in raw_data:
        data.append({"username":cur[0],"user_id":cur[1]})
    return jsonify(data)

@app.route('/register/<string:username>/<string:password>') #register
def register(username,password,):
    password = bcrypt.generate_password_hash(password)
    cur = mysql.connection.cursor() 
    cur.execute(""" SELECT username FROM users WHERE username = %s """, [username])
    users_name = cur.fetchall()
    if len(users_name) < 1:
        cur.execute("""INSERT INTO users (username,password) VALUES (%s, %s)""", [username, password])
        mysql.connection.commit()
        cur.close()
        return "Registered"
    else :
        mysql.connection.commit()
        cur.close()
        return "Username already exists"

@app.route('/admin/<string:username>/<string:password>') 
def admin(username,password,):
    password = bcrypt.generate_password_hash(password)
    cur = mysql.connection.cursor() 
    cur.execute(""" SELECT username FROM admin WHERE username = %s """, [username])
    users_name = cur.fetchall()
    if len(users_name) < 1:
        cur.execute("""INSERT INTO admin (username,password) VALUES (%s, %s)""", [username, password])
        mysql.connection.commit()
        cur.close()
        return "Registered"
    else :
        mysql.connection.commit()
        cur.close()
        return "admin already exists"

@app.route('/deluser/<string:user_id>')
def delete_user(user_id):  
    cur = mysql.connection.cursor() 
    cur.execute("DELETE FROM users WHERE user_id = %s ", [user_id])
    mysql.connection.commit()
    cur.close() 
    return "Deleted!"

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

@app.route('/adminlogin/<string:username>/<string:password>') #login
def adminlogin(username,password,):
    check_password = None
    user_data = []
    cur = mysql.connection.cursor() 
    cur.execute(""" SELECT username,password FROM admin WHERE username = %s  """, [username] )
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

@app.route('/sent/<string:farm_id>/<string:temp>/<string:humid>') #???????????????? #server????????????
def sent(farm_id,temp,humid):
    if temp != 'nan':
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
        def Average(i):
            avg = sum(i) / len(i)
            return avg
        tempdata = round(Average(tempdata),2)
        humiddata = round(Average(humiddata),2)
        cur.execute(""" UPDATE farm SET temp=%s, humid=%s, time=%s WHERE farm_id = %s """, (tempdata, humiddata, time_now, farm_id) )
        mysql.connection.commit()
        cur.close() 
        return "Sent!"  
    else :
        return ("NAN")

@app.route('/read/<string:user_id>') #????????????????
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

@app.route('/read/farm/<string:farm_id>') 
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

@app.route('/change-option/<string:farm_id>/<string:Automate>/<string:fix_temp>/<string:fix_humid>/<string:fan_status>/<string:fog_status>')
def change_option(farm_id,Automate,fix_temp,fix_humid,fan_status,fog_status):
    cur = mysql.connection.cursor()
    cur.execute(""" UPDATE farm SET Automate=%s,fix_temp = %s,fix_humid = %s,fan_status = %s,fog_status = %s WHERE farm_id = %s """, (Automate,fix_temp,fix_humid,fan_status,fog_status, farm_id) )
    mysql.connection.commit()
    cur.close()
    return "Success!" 

@app.route('/check-condition/<string:farm_id>') #????????????
def check_condition(farm_id): 
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
        if temp >= fix_temp : 
            fan_status = 1 
        elif temp <= fix_temp - 1 :  
            fan_status = 0
#-------------------------------------------------#
        if humid <= fix_humid :
            fog_status = 1
        elif humid >= fix_humid + 10 :
            fog_status = 0

    elif Automate == 0 :
        fog_status = fog_status
        fan_status = fan_status
    else :
        return ("Error")

    cur.execute(""" UPDATE farm SET fan_status = %s, fog_status = %s WHERE farm_id = %s """, (fan_status,fog_status,farm_id,) )
    mysql.connection.commit()
    cur.close()
    raw_data = (fan_status,fog_status)
    return str(raw_data)

@app.route('/statistic/<string:farm_id>') 
def statistic(farm_id):
    tempdata = []
    humiddata = []
    cur = mysql.connection.cursor()
    time_now = datetime.datetime.now()
    time_hr = (time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour)+datetime.timedelta(hours=time_now.minute//30))
    time = time_now - datetime.timedelta(hours=1)
    cur.execute(""" SELECT temp,humid FROM farm_details WHERE farm_id = %s and datetime > %s ORDER BY id DESC """, [farm_id, time] )
    raw_data = cur.fetchall()
    for i in range(len(raw_data)) :
        tempdata.append(raw_data[i][0])
        humiddata.append(raw_data[i][1])
    def Average(i):
        avg = sum(i) / len(i)
        return avg
    tempdata = Average(tempdata)
    humiddata = Average(humiddata)
    tempdata = round(tempdata,2)
    humiddata = round(humiddata,2)
    cur.execute("""INSERT INTO statistic (farm_id,temp,humid,time) VALUES (%s, %s, %s, %s)""", (farm_id, tempdata, humiddata, time_hr))
    cur.execute("""DELETE FROM farm_details WHERE farm_id = %s and datetime < %s""", (farm_id, time))
    mysql.connection.commit()
    cur.close() 
    return "Sent!" 

@app.route('/statistic/<string:farm_id>/<string:time>') 
def statistic_farm(farm_id,time):
    data_time = time.split("-")
    time = datetime.datetime( int(data_time[0]),int(data_time[1]),int(data_time[2]) ) 
    oneday = time + datetime.timedelta(days=1) 
    data = []
    cur = mysql.connection.cursor()
    cur.execute(""" SELECT * FROM statistic WHERE farm_id = %s and time >= %s and time < %s """, [farm_id,time,oneday] )
    raw_data = cur.fetchall()
    cur.close()
    for cur in raw_data:
        time = cur[4].strftime("%H:%M")
        data.append({"id":cur[0],"farm_id":cur[1],"temp":cur[2],"humid":cur[3],"time":time})
    return jsonify(data)

    cur = mysql.connection.cursor()
    cur.execute(""" SELECT testtest FROM test ORDER BY testtest DESC LIMIT 1""")
    data = cur.fetchall()
    numm = data[0][0]
    numtest = numm + 1
    cur.execute("""INSERT INTO test (testtest) VALUES (%s)""", [numtest])
    mysql.connection.commit()
    cur.close()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)