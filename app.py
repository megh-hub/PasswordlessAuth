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
cred=credentials.Certificate('blockchain-nis-firebase-adminsdk-kg1u8-26cecdacc3.json')
default_app = initialize_app(cred)
db = firestore.client()
# ----------------------------the core flask app with all redirections--------------------
app = Flask(__name__,template_folder='templates')
print("here")

@app.route("/")
def home():
    return render_template("index.html")
    print("Megha");
mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp..com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'webi.fi.tech@gmail.com'
app.config['MAIL_PASSWORD'] = 'webtech123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = random.randint(1000, 9999)
email = 'useremail@gmail.com'
gen_privateKey ="MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDE0LyKHArPLrWC\nfcUa7TMl7ZYQB51EYAdrdAMQO3PTGFTmlHW0hMj8hH0vmOHyZEnvuR5gpGIqiAsI\n4nZkCscVeA3RVRtgXlefSy44XIPtecSuaIKkdbJlSg8LcuXX/dZq/WLQ+JIn2MZP\nborAUpgbjN32+CA57tOMTViCvwTENqWoyxprjPV/8EajWt/UjGH/ecIGI+uAZBrO\nFOOHY6aF18fpJivH0H40QZhN8zfu7/55LUuKiiV9LsKHUBrvrkZHgh/Yb0CjunDG\ndR2wnkSylXUFxk+K1v7iwHbiEWtFPy2VfuYrbIzZdS1S1Jd1lGm8nKOHqLotorY5\nLUGLU23XAgMBAAECggEACzHS7N7IH/KzMPdAZStavmyIyDlL+7NOmLu3ijkneblS\nPZnyJqYVhy9uA21kZKoe/ntUEVZ9nZexW6cDPuYnXr7pDPVp942bhEb9cQfqGnF+\nUMFHCl2wxkwea530bthUVYTmFabIgWsLaeyKsy0U08mrvRFt8ShMG23cJqEA1Lws\nDEKmok09/6/wbS1DB/y4AaER3m2+HnMT0az8DPisB2sRzsHJqlVzdzCcvBtRnd4t\n1VW3v+a6OLnnC9lNyMMndPw1kaqQRsUsf1JuV3afUkVgwLzLgOINy/vBXtfLFoOa\ncV64npIQ2Cg6nTkmmRUsyLti6mgEqnC4OWnhE5GuYQKBgQDyd5YRsQrglJ8qr0kl\nUalAFi/DcA1AX/ynSnyF3Spa3UkUPRDiHTZx545lNTGvCTBVW0TCflgIkn82T3Qv\nnubXsGDOyqaYAaNqMQqZzDvE3xxHu9pCaHejAGUsFvgawM+eT+FSAKHlubgUG4RS\ncXoJFaUqcWykQEQgDVCbUG2mJwKBgQDPzN6rla7/c5LYzbNyCpWqsHdU/eg0wybm\nijOXeFDONGWv3HVnmcSp457yCMvyWPpC8BwPJs8kk8eTsrIe9IGNBulI9WrxeaHH\nKXZ85PuAJ2SMt5UXY5lX2kicaFrb1tJuxGzjcdLpRCeVmjkANbmw/HqlE4+XHtXU\nolfdmP/40QKBgGvXrqKtyPW8hNK6ZeE4YfwEIjhd9Tblun05zwrHJNiHRcK/qmu3\nrIibAiWXtEJy5tGAJ6QOB9/AMN6aFkY7+daDN3uifNhtGh7YMyvWv9q/lVd+gQQ6\nbMPOIDGtAar8iRuT0dbkOx3vLaWb243DtRCnVO/8xOKFRweuhGSgMDTPAoGAE+fm\nNL2kA+iIWqhp1jTZXX6GD+g6xEMliNQYWRw3cWlnjE8sF/6M7lFVuo3JK7AGWT8z\nEOiA01ostiNaGMkHWAEfe9O2qOcj7jY0mYY96WrcoPY9G/54hAfvCLyeZ4zOn7nF\nTIxszdeviw85AqIi5adqAEI9cRaNGU9r51huvOECgYEAjSP6wzKZZdoeddBE4T5F\n8HLyqEymn7KwVEulMyikER3g49McwvG8rYYo0pTsXwYWozw3Al0G/gfDoiso8ToE\nOhHYqltFzoQ5T9wxZE8VHmm16//+1atBh0yw/5JLGxwjk5gisNQAQyn9k2S3/vlI\nufmWbdqpNVAPSkgTW0ltOyg"
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
