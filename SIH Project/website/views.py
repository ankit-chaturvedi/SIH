from flask import Blueprint, Flask, render_template, request
import pymongo

views = Blueprint('views', __name__)

# connecting to the Mongo DB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
#get the database name
db  = client.get_database('total_records')
record = db.tips

@views.route('/anonymous_tip/', methods = ['GET', 'POST'])
def tip():

    if request.method == 'POST':

        type = request.form.get('type')
        contact = request.form.get('contact')
        desc = request.form.get('desc')
        pincode = request.form.get('pincode')

        anynomous_input = {'type':type, 'contact':contact, 'desc':desc, 'pincode':pincode}
        record.insert_one(anynomous_input)

        message = 'successfully sent :)'
        return render_template('tips.html', message = message)
    return render_template('tips.html')