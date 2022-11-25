from flask import Flask,render_template,request
from loc import loc
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        city = request.form.get('city')
        subject = request.form.get('subject')
        feedback = request.form.get('feedback')

        print(city,subject,feedback)
    return str(loc())

if __name__ == "__main__":
    app.run(debug=True)