'''
firebase project - NISCoinBlock
'''
from pickle import NONE
from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, jsonify, request, send_file,session
from flask_cors import CORS
from flask_session import Session
import qrcode
from io import BytesIO
from flask import *
from flask_mail import *
import random
import pyrebase
from flask_qrcode import QRcode
from time import sleep
import datetime
import hashlib
import json
import os
import rsa
import urllib

from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# import google.cloud
# from google.cloud import firestore
# ---------------------integrating firebase in our flask app---------------------
cred=credentials.Certificate('niscoinblock-firebase-adminsdk-yg3l1-6265245b34.json')
default_app = initialize_app(cred)
db = firestore.client()
# ----------------------------the core flask app with all redirections--------------------
app = Flask(__name__)
print("here")

@app.route("/")
def home():
    return render_template("index.html")
mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'webi.fi.tech@gmail.com'
app.config['MAIL_PASSWORD'] = 'webtech123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = random.randint(1000, 9999)
email = 'useremail@gmail.com'
gen_privateKey ="MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4lyUMAk234khudJVLKneRc/4knOCjQNagKb760BE54zmPAC6gjwZaO7PRWTPiSsfiOvFhGczod3bN47rJAHPGTgldIxxxarISf2JKE5sp8vwH9BRgplp25DcpPBTN9ZHx6bR4+ctN93aNdqjjXs15VJs0D+8rFmwr6OKD4Mms+7mQlDATXwh2HuVfbXCCAstUAapcxW01uxlc2IDeoXqWlHE1yCYZDkzHh7BJi/Yt52Tsm40MQmIY2IPGhryoje7Y48GRWu06dzX3/brl/xFqnLVSx/OM/Ts/n8VlnGtJlIyvhcs6Tq7AA/RQRac9t5mn8+ztYNZzpd0SfukuMRtbAgMBAAECggEBAI2QdPwJxDrTEsOLK3fzALIPaAgCPBFXx4IbofjOm3duuRTfieLe7XtEMDrMk4rn2PW6SKY0WD6sZ/Osw/IlI6Ug8fN42vZsYlbnVKUE9kmsrPcYjIw26Egn69n21unBfIUvu5XP1MhdkZEaQJnneeOkLEc4NS8xShI+z4FeYq0DLxEpkZzs+B7d0R6qRcuq1XkiI96iDbapnMXd/pFrYxSojBJxrY2LaBcOImKPqDmb0vqh6f30pSMuvfyR+S1ignpih3qwwxYxNdPGoMZJCW/d8i5+xd0x6P7DgRN0hAsQsW1a1Np5e4aAegIBMpxxvnGqHTHDoxiQAICcQkWbXRECgYEA39k7ThNEMnQH60+9g5jo5IIdF2BO3P48aghpV2ES8k+YxlQDEMkPd/jWQgCUaQ6s5znRO443wLn5dEpcSt6l38PLX/ONAzDMNC0f/s/4ORQH04F8uWuGYoNe0s1qyshWH0vSQpr9uHk9HsuLW9t+ajwMn21dvBlKDJe2o7/cC+kCgYEA0xpqegLCuD47q3j56kMk+Ap3pXySspVesOGAp924eqhCS0yKC6d8NR3K6n6ZtMsQjx2UT0hQHorFpgojyJlXprQhxOgCUP27jODaIs4qLKUVmkIJacuHguSFCYUpbyl5u4Ref4OFEU/4ZTyhIT9pxucQglhGMGGGSwjAkMNjlqMCgYEA2L9dP1JEfJ4BdQY3OQ98opaiWJo2gqHiGcGfTq5+TAZqpc9/UGd/BOn7fNlW2wsMvLAtOv+QWJs7QjEmgJBqCOtrJ7OKXQaJFBSFoJP7hDkzAsek312QOB+AV5nzx/qH+bHPHBM7jb5HQmRQwlccZv1SM6UQWCwcmWjlvlTuWtECgYAvMVmaWyGixK7cP5hHKamLFfP3d+jnqYLYsiDr5iJGsXTYlozJ3DBlQ3rIf3LnOvpBtFAihTz8BvP2kY+8WaOBrgVamq9h4cda0C2T2FkPT/yLVrX6A7kQpvuizDUeF7ySEh56DTHjU+ho4Wv4HdAM2j0Tlp5iVHsMLTG3aybJVwKBgHyLIrvIqFmkAyrjOTQVfRgdnck8UE8hT0wY3K2A1bXFtgfmKp4vMsT7/KHNZZOCgN95BF1xs2VrSVAa9TBJzv3viqqTjUJwiKa9zNgjr166b8QkFZI0urDHn19owMiJ3fR1qyazESHGZSEv7VYNX/yiJL+PmO57GRlC2buAgeAb"
# ----------------------------------------------- REGISTER METHOD-----------------------------------
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        global email
        email = request.form["email"]
        msg = Message('OTP', sender='webi.fi.tech@gmail.com', recipients=[email])
        msg.body = str(otp)
        mail.send(msg)
        return render_template("verify.html")
# ---------------------------- validate OTP -----------------------------------------------
CORS(app)
@app.route("/validate", methods=["POST"])
def validate():
    givenotp = request.form['givenotp']
    if otp == int(givenotp):
        global email
        qr = qrcode.make(email)
        qr.save("static/img/currQR.png")
        sleep(10)
        return render_template("validateQR.html", user=email)
    return "<h1>NOT Verified!</h1>"

@app.route("/validateLogin", methods=["POST"])
def validateLogin():
    givenotp = request.form['givenotp']
    if otp == int(givenotp):
        global email
        qr = qrcode.make(email)
        qr.save("static/img/currQR.png")
        sleep(10)
        return render_template("validateQRLogin.html")
    return "<h1>NOT Verified!</h1>"
# ------------------------------- validate firestore (after qr code) -------------------------
@app.route("/validateFirestore", methods=["GET"])
def validateFirestore():
    global email
    print("logging: email in register ============== ", email)
    docs = db.collection(u'SignUP').where(u'email', u'==', email).stream()
    currentUser = dict()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        currentUser = doc.to_dict()
    if currentUser:
        if (currentUser["success"] == "true"):
            return render_template("dashboard.html", user=email)
        return "not validated"
    else:
        return "<h3>you must validate on your phone before moving forward!</h3>"

@app.route("/validateLoginFirestore", methods=["GET"])
def validateLoginFirestore():
    global email
    docs = db.collection(u'Login').where(u'email', u'==', email).stream()
    currentUser = dict()
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
        currentUser = doc.to_dict()
    if currentUser:
        if (currentUser["success"] == "true"):
            return render_template("dashboard.html", user=email)
        return "not validated"
    else:
        return "< h3 > you must create an account and validate on your phone before logging in !</h3 >"
    
# ------------------------------------- BLK METHODS---------------------------------------------
def checkEquality(original, decrypted):
    if original == decrypted:
        print("logging.... true")
    return True
url = "https://ngrok.8231.io"
def helperFun(decryptedMessage):
    retrievedPublicKey = ""
    completeURL = url + "/searchPublicKey?" + decryptedMessage
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    retrievedPublicKey = dict["publicKey"]
    # calling searchPublicKey to retrieve the public key
    timestamp = time.time()
    # hashing the timestamp
    msgHash = hashlib.sha256(timestamp.encode()).hexdigest()
    # encrypting the timestamp
    cipherText = rsa.encrypt(msgHash.encode('ascii'), retrievedPublicKey)
    pushToFirebase(cipherText)
    finalMessage = ""
    while (True):
        # check android app
        docs = db.collection(u'thirdRound').where(u'email', u'==', email).stream()
        messageObj = docs.stream()
        if (messageObj is not None):
            finalMessage = messageObj.to_dict()["hash"]
            break
    decryptPKa = rsa.decrypt(finalMessage, gen_privateKey).decode('ascii')
    decryptPUb = rsa.decrypt(decryptPKa, retrievedPublicKey).decode('ascii')
    # decrypt the final message first with your private key and then with user's public key then
    # return true or false based on the comparison between the decrypted message and the original message
    # which is msgHash
    return checkEquality(msgHash, decryptPUb)


def pushToFirebase(cipherText):

    # check android code
    doc_ref = db.collection(u'secondRound').document()
    doc_ref.set({
        u'message': cipherText
    })

@app.route('/getWebsitePublicKey', methods=["GET"])
def getWebsitePublicKey(decryptedHash):
    store_blocks = open("blocks.txt", "a+")
    store_blocks.seek(0)
    read_blocks = store_blocks.readlines()
    websitePublicKey = ""
    for line in read_blocks:
        curr = [x for x in line.strip().split()]
        websitePublicKey = curr[3]
        break
    data = {"publicKey": websitePublicKey}
    return jsonify(data)

def decryptMessage():
    global email
    docs = db.collection(u'FirstRound').where(u'email', u'==', email).stream()
    currentUser = dict()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        currentUser = doc.to_dict()
    currHash = currentUser["hash"]
    decryptedHash = rsa.decrypt(currHash, gen_privateKey).decode('ascii')
    return decryptedHash
    # getPublicKey(decryptedHash)
    
@app.route('/validateLoginBlock', methods=["GET"])
def validateLoginBlock():
    decryptedData = decryptMessage()
    res = helperFun(decryptedData)
    if res:
        return render_template("dashboard.html", user=email)
    return "< h3 > you must create an account and validate on your phone before logging in !< /h3 >"
# --------------------------------------- LOGIN METHOD--------------------------------------------


@app.route("/login", methods=["POST", "GET"])
def login():
    # return render_template("login.html")
    if request.method == 'GET':
        return render_template("login.html")
    else:
        global email
        email = request.form["email"]
        msg = Message('OTP', sender='webi.fi.tech@gmail.com', recipients=[email])
        msg.body = str(otp)
        mail.send(msg)
        return render_template("verifyLogin.html")
    
if __name__ == "__main__":
    app.run(debug=True)
