from flask import Flask, render_template,request,session,url_for,redirect
import pymongo
import bcrypt,random


app = Flask(__name__)
app.secret_key = 'dsgfjgnje dfsfdgdsg'


# connecting to the Mongo DB database
client = pymongo.MongoClient("mongodb://localhost:27017/")

#get the database name
db  = client.get_database('total_records')
records = db.register

def genrandom():
    n = ''
    x=0
    while x<7:
        y = random.randint(1,9)
        if str(y) not in n:
            n+=str(y)
            x+=1
    return str(n)

def userid():
    n = genrandom()
    if records.find_one({"userid":n}):
        print('already exists')
        userid()
    else:
        return n
        

#assigning URL to have the sign-up route
@app.route('/auth/sign-up/', methods = ['GET', 'POST'])
def sign_up():
    if "user" in session:
        return redirect(url_for('logged_in'))

    if request.method == 'POST':
        email = request.form.get('email')
        PS_loc = request.form.get('PS_loc')
        Pincode = request.form.get('Pincode')

        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_pass')
        UserId = userid()
        #Checking whether email is already registered or not
        email_found = records.find_one({"email":email})
        
        if email_found:
            message = 'This email already exists'
            return render_template('sign_up.html', message = message)

        if password!=confirm_pass:
            message = 'Passwords should match!'
            return render_template('sign_up.html',message = message)
        
        else:
            #hashing the password and encoding it
            hashed = bcrypt.hashpw(confirm_pass.encode('utf-8'), bcrypt.gensalt())

            #assigning the data in a dictionary in key value pairs
            user_input = { 'userid':UserId, 'email': email, 'password': hashed, 'PS_loc': PS_loc, 'Pincode':Pincode}
            #inserting it in the record collection
            records.insert_one(user_input)

            user_data = records.find_one({"email":email})
            new_email = user_data['email']

            message = 'Check your registered email'
            return render_template('sign_up.html', message = message)
    return render_template('sign_up.html')

@app.route('/auth/login/', methods = ['GET','POST'])
def login():
    message = "Please login to your account"

    if "user" in session:
        return redirect(url_for("logged_in"))

    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')

        #check if User Id exists in database
        user_found = records.find_one({"userid":str(userid)})
        if user_found:
            user_val = user_found['userid']
            passwordcheck = user_found['password']

            #encode the password and check if it matches or not
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["userid"] = user_val
                return redirect(url_for('logged_in'))
            else:
                if "user" in session:
                    return redirect(url_for('logged_in'))
                message = "Wrong password"
                return render_template('login.html',message = message)
        else:
            message = 'User not found'
            return render_template('login.html', message = message)
    return render_template('login.html', message = message)


@app.route('/logged_in/')
def logged_in():
    if "user" in session:
        user = session["user"]
        return render_template('logged_in.html',user = user)
    else:
        return redirect(url_for("login"))

@app.route("/auth/logout/", methods = ['POST','GET'])
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug = True)