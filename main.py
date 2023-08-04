# STEP-1: pip install opencv-python
from flask import Flask ,render_template,request,flash,redirect,url_for
import os
import cv2
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail, Message

local_server = True

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

with open("static/config.json",'r')as c:
    params=json.load(c)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'C:\\DATA\\image editing app with gui python\\uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/fukra Editing'
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL='True',
    MAIL_USERNAME='gmail_user',
    MAIL_PASSWORD='gmail_pass'
)
mail = Mail(app)
# SECRET_KEY = 'the '
app.secret_key="THE"

class contacts(db.Model):
    name = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, unique=True)
    message = db.Column(db.String, unique=True)
    email = db.Column(db.String)


                    #CONTACT PAGE 
@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        sub = request.form.get("sub")
        msg = request.form.get("msg")
        email = request.form.get("email")
     
        entry=contacts(name=name, subject=sub, message=msg, email=email)
        db.session.add(entry)
        db.session.commit()
        msg = Message('Hello from the other side!', 
                    sender =   'email',
                    recipients = 'gmail_user')
        msg.body = "Hey {name}, sending you this email from my Flask app, lmk if it works"
        mail.send_message(msg)
        # return "Message sent!"
    return render_template("contact.html")



'''           PROCESSING THE IMAGE      '''
def process_image(filename,Operation):
    print(f"The operation is {Operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")

    '''Convert to cgray'''
    match Operation:
        case "cgray":
            newfilename=f"static/assets/{filename}"
            imgprocessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(newfilename,imgprocessed)
            return newfilename
         
        # case "ctxt":
        #     newfilename="static/{filename}"
        #     cv2.imwrite(f"static/{filename.split('.')[0]}.txt",img)
        #     return newfilename
        
        # case "cpdf":
        #     newfilename="static/{filename}"
        #     cv2.imwrite(f"static/{filename.split('.')[0]}.pdf",img)
        #     return newfilename
        
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        
        case "cjpg":  
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        
        # case "cgif":
        #     newfilename="static/{filename}"
        #     cv2.imwrite(f"static/{filename.split('.')[0]}.gif",img)
        #     return newfilename
        
        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
    pass

def allowed_file(filename): 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''             HOME PAGE     ''' 
@app.route("/")
def home():
    return render_template("index.html")

                    #EDIT PAGE 
@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        Operation=request.form.get("Operation")
        '''check if the post request has the file part'''
        if 'file' not in request.files:
            flash('No file part')
            return render_template("error.html")
        file = request.files['file']
        ''' If the user does not select a file, the browser submits an
            empty file without a filename.'''
        if file.filename == '':
            flash('No selected file')
            return "error no file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=process_image(filename,Operation)
            flash(f"your image has been processed and available here <a href='/{new}' target='_blank' >Show preview</a>")
            return render_template("index.html")
            # return redirect(url_for('download_file', name=filename))
    return render_template("index.html")

                    #ABOUT PAGE 
@app.route("/about")
def about():
    return render_template("about.html")



                    #DOCUMENTATION (HOW TO USE) PAGE 
@app.route("/doc")
def doc():
    return render_template("doc.html")



app.run(debug=True)