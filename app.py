'''
firebase project - NISCoinBlock
'''
import ssl
import smtplib
from email.mime.text import MIMEText
from ast import dump
from pickle import NONE
from venv import create
from wsgiref.simple_server import server_version
from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, jsonify, request, send_file, session
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
import urllib3
import threading

from flask import Flask, request, jsonify
# from flask_ngrok import run_with_ngrok
from firebase_admin import credentials, firestore, initialize_app

# import google.cloud

# from google.cloud import firestore
# ---------------------integrating firebase in our flask app---------------------
cred = credentials.Certificate(
    'blockchain-nis-firebase-adminsdk-kg1u8-26cecdacc3.json')
default_app = initialize_app(cred)
db = firestore.client()
# ----------------------------the core flask app with all redirections--------------------
app = Flask(__name__, template_folder='templates')
# run_with_ngrok(app)
print("here")


@app.route("/")
def home():
    return render_template("index.html")
    print("Megha");


mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.mailtrap.io'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'a4844eac8a7f74'
app.config['MAIL_PASSWORD'] = '1a8b2caab6b2f2'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = random.randint(1000, 9999)
email = 'useremail@gmail.com'
gen_privateKey = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDE0LyKHArPLrWC\nfcUa7TMl7ZYQB51EYAdrdAMQO3PTGFTmlHW0hMj8hH0vmOHyZEnvuR5gpGIqiAsI\n4nZkCscVeA3RVRtgXlefSy44XIPtecSuaIKkdbJlSg8LcuXX/dZq/WLQ+JIn2MZP\nborAUpgbjN32+CA57tOMTViCvwTENqWoyxprjPV/8EajWt/UjGH/ecIGI+uAZBrO\nFOOHY6aF18fpJivH0H40QZhN8zfu7/55LUuKiiV9LsKHUBrvrkZHgh/Yb0CjunDG\ndR2wnkSylXUFxk+K1v7iwHbiEWtFPy2VfuYrbIzZdS1S1Jd1lGm8nKOHqLotorY5\nLUGLU23XAgMBAAECggEACzHS7N7IH/KzMPdAZStavmyIyDlL+7NOmLu3ijkneblS\nPZnyJqYVhy9uA21kZKoe/ntUEVZ9nZexW6cDPuYnXr7pDPVp942bhEb9cQfqGnF+\nUMFHCl2wxkwea530bthUVYTmFabIgWsLaeyKsy0U08mrvRFt8ShMG23cJqEA1Lws\nDEKmok09/6/wbS1DB/y4AaER3m2+HnMT0az8DPisB2sRzsHJqlVzdzCcvBtRnd4t\n1VW3v+a6OLnnC9lNyMMndPw1kaqQRsUsf1JuV3afUkVgwLzLgOINy/vBXtfLFoOa\ncV64npIQ2Cg6nTkmmRUsyLti6mgEqnC4OWnhE5GuYQKBgQDyd5YRsQrglJ8qr0kl\nUalAFi/DcA1AX/ynSnyF3Spa3UkUPRDiHTZx545lNTGvCTBVW0TCflgIkn82T3Qv\nnubXsGDOyqaYAaNqMQqZzDvE3xxHu9pCaHejAGUsFvgawM+eT+FSAKHlubgUG4RS\ncXoJFaUqcWykQEQgDVCbUG2mJwKBgQDPzN6rla7/c5LYzbNyCpWqsHdU/eg0wybm\nijOXeFDONGWv3HVnmcSp457yCMvyWPpC8BwPJs8kk8eTsrIe9IGNBulI9WrxeaHH\nKXZ85PuAJ2SMt5UXY5lX2kicaFrb1tJuxGzjcdLpRCeVmjkANbmw/HqlE4+XHtXU\nolfdmP/40QKBgGvXrqKtyPW8hNK6ZeE4YfwEIjhd9Tblun05zwrHJNiHRcK/qmu3\nrIibAiWXtEJy5tGAJ6QOB9/AMN6aFkY7+daDN3uifNhtGh7YMyvWv9q/lVd+gQQ6\nbMPOIDGtAar8iRuT0dbkOx3vLaWb243DtRCnVO/8xOKFRweuhGSgMDTPAoGAE+fm\nNL2kA+iIWqhp1jTZXX6GD+g6xEMliNQYWRw3cWlnjE8sF/6M7lFVuo3JK7AGWT8z\nEOiA01ostiNaGMkHWAEfe9O2qOcj7jY0mYY96WrcoPY9G/54hAfvCLyeZ4zOn7nF\nTIxszdeviw85AqIi5adqAEI9cRaNGU9r51huvOECgYEAjSP6wzKZZdoeddBE4T5F\n8HLyqEymn7KwVEulMyikER3g49McwvG8rYYo0pTsXwYWozw3Al0G/gfDoiso8ToE\nOhHYqltFzoQ5T9wxZE8VHmm16//+1atBh0yw/5JLGxwjk5gisNQAQyn9k2S3/vlI\nufmWbdqpNVAPSkgTW0ltOyg"
# ----------------------------------------------- REGISTER METHOD-----------------------------------


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        global email
        email = request.form["email"]
        # msg = Message('OTP', sender='webi.fi.tech@gmail.com', recipients=[email])
        # msg.body = str(otp)
        # #dump(msg)
        # mail.send(msg)

        msg = MIMEText(str(otp))
        msg['Subject'] = "OTP"
        msg['To'] = email
        msg['From'] = 'eshan_bajaj@yahoo.com'

        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        # context = ssl.create_default_context()
        server.ehlo()
        # server.starttls(context=context)
        server.starttls()
        server.ehlo()
        server.login('eshan_bajaj@yahoo.com', 'iilbelaabmukqhcf')
        # server.sendmail('eshan_bajaj@yahoo.com',email, "Subject: TEST")
        server.sendmail('eshan_bajaj@yahoo.com', email, msg.as_string())
        server.quit()
        return render_template("verify.html")


# ---------------------------- validate OTP -----------------------------------------------
CORS(app)


@app.route("/validate", methods=["POST"])
def validate():
    givenotp = request.form['givenotp']
    if otp == int(givenotp):
        global email
        qr = qrcode.make(email)
        qr.save("static/currQR.png")
        sleep(10)
        return render_template("validateQR.html", user=email)
    return "<h1>NOT Verified!</h1>"


@app.route("/validateLogin", methods=["POST"])
def validateLogin():
    givenotp = request.form['givenotp']
    if otp == int(givenotp):
        global email
        qr = qrcode.make(email)
        qr.save("static/currQR.png")
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


url = "https://wet-jobs-warn-157-51-18-111.loca.lt"


@app.route("/updateUrl")
def update_url():
    global url
    url = request.args.get('url', default=url, type=str)


def helperFun(decryptedMessage):
    retrievedPublicKey = ""
    completeURL = url + "/searchPublicKey?" + decryptedMessage
    response = urllib3.request.urlopen(url)
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
        docs = db.collection(u'thirdRound').where(
            u'email', u'==', email).stream()
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
        msg = Message('OTP', sender='webi.fi.tech@gmail.com',
                      recipients=[email])
        msg.body = str(otp)
        mail.send(msg)
        return render_template("verifyLogin.html")


# run_with_ngrok(app)
# ------------- creating block ------------------


# class NISCoinBlock:
#     def __init__(self, prev_hash, imei, publicKey):
#         self.prev_hash = prev_hash
#         self.imei = imei
#         self.publicKey = publicKey
#         # generating hash of the imei code
#         self.block_hash = hashlib.sha256(self.imei.encode()).hexdigest()
# @app.route("/getHash", methods=["GET"])
# def getHash():
#     args = request.args
#     print(args) #for debugging
#     email = args['email']
#     imei = args['imei']
#     publicKey = args['publicKey']
#     print("DETAILS ARE........", email, imei, publicKey)
#     # read already stored blocks
#     store_blocks = open("blocks.txt", "a+")
#     store_blocks.seek(0)
#     all_blocks = dict()
#     last_block = []
#     read_blocks = store_blocks.readlines()
#     for line in read_blocks:
#         curr = [x for x in line.strip().split()]key = curr[0] #email
#  value = [curr[1], curr[2], curr[3]] #prev_hash, imei, publicKey
#  all_blocks[key] = value
#  last_block = curr
#  # create genesis block
#  print(all_blocks)
#  gen_hash = ""
#  gen_publicKey ="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuJclDAJNt+JIbnSVSyp3kXP+JJzgo0DWoCm++tAROeM5jwAuoI8GWjuz0Vkz4krH4jrxYRnM6Hd2zeO6yQBzxk4JXSMccWqyEn9iShObKfL8B/QUYKZaduQ3KTwUzfWR8em0ePnLTfd2jXao417NeVSbNA/vKxZsK+jig+DJrPu5kJQwE18Idh7lX21wggLLVAGqXMVtNbsZXNiA3qF6lpRxNcgmGQ5Mx4ewSYv2Ledk7JuNDEJiGNiDxoa8qI3u2OPBkVrtOnc19/265f8Rapy1UsfzjP07P5/FZZxrSZSMr4XLOk6uwAP0UEWnPbeZp/Ps7WDWc6XdEn7pLjEbWwIDAQAB"
#  gen_privateKey ="MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4lyUMAk234khudJVLKneRc/4knOCjQNagKb760BE54zmPAC6gjwZaO7PRWTPiSsfiOvFhGczod3bN47rJAHPGTgldIxxxarISf2JKE5sp8vwH9BRgplp25DcpPBTN9ZHx6bR4+ctN93aNdqjjXs15VJs0D+8rFmwr6OKD4Mms+7mQlDATXwh2HuVfbXCCAstUAapcxW01uxlc2IDeoXqWlHE1yCYZDkzHh7BJi/Yt52Tsm40MQmIY2IPGhryoje7Y48GRWu06dzX3/brl/xFqnLVSx/OM/Ts/n8VlnGtJlIyvhcs6Tq7AA/RQRac9t5mn8+ztYNZzpd0SfukuMRtbAgMBAAECggEBAI2QdPwJxDrTEsOLK3fzALIPaAgCPBFXx4IbofjOm3duuRTfieLe7XtEMDrMk4rn2PW6SKY0WD6sZ/Osw/IlI6Ug8fN42vZsYlbnVKUE9kmsrPcYjIw26Egn69n21unBfIUvu5XP1MhdkZEaQJnneeOkLEc4NS8xShI+z4FeYq0DLxEpkZzs+B7d0R6qRcuq1XkiI96iDbapnMXd/pFrYxSojBJxrY2LaBcOImKPqDmb0vqh6f30pSMuvfyR+S1ignpih3qwwxYxNdPGoMZJCW/d8i5+xd0x6P7DgRN0hAsQsW1a1Np5e4aAegIBMpxxvnGqHTHDoxiQAICcQkWbXRECgYEA39k7ThNEMnQH60+9g5jo5IIdF2BO3P48aghpV2ES8k+YxlQDEMkPd/jWQgCUaQ6s5znRO443wLn5dEpcSt6l38PLX/ONAzDMNC0f/s/4ORQH04F8uWuGYoNe0s1qyshWH0vSQpr9uHk9HsuLW9t+ajwMn21dvBlKDJe2o7/cC+kCgYEA0xpqegLCuD47q3j56kMk+Ap3pXySspVesOGAp924eqhCS0yKC6d8NR3K6n6ZtMsQjx2UT0hQHorFpgojyJlXprQhxOgCUP27jODaIs4qLKUVmkIJacuHguSFCYUpbyl5u4Ref4OFEU/4ZTyhIT9pxucQglhGMGGGSwjAkMNjlqMCgYEA2L9dP1JEfJ4BdQY3OQ98opaiWJo2gqHiGcGfTq5+TAZqpc9/UGd/BOn7fNlW2wsMvLAtOv+QWJs7QjEmgJBqCOtrJ7OKXQaJFBSFoJP7hDkzAsek312QOB+AV5nzx/qH+bHPHBM7jb5HQmRQwlccZv1SM6UQWCwcmWjlvlTuWtECgYAvMVmaWyGixK7cP5hHKamLFfP3d+jnqYLYsiDr5iJGsXTYlozJ3DBlQ3rIf3LnOvpBtFAihTz8BvP2kY+8WaOBrgVamq9h4cda0C2T2FkPT/yLVrX6A7kQpvuizDUeF7ySEh56DTHjU+ho4Wv4HdAM2j0Tlp5iVHsMLTG3aybJVwKBgHyLIrvIqFmkAyrjOTQVfRgdnck8UE8hT0wY3K2A1bXFtgfmKp4vMsT7/KHNZZOCgN95BF1xs2VrSVAa9TBJzv3viqqTjUJwiKa9zNgjr166b8QkFZI0urDHn19owMiJ3fR1qyazESHGZSEv7VYNX/yiJL+PmO57GRlC2buAgeAb"
#  if last_block == []:
#  # create genesis block
#  print("creating first block...")
#  gen_block = NISCoinBlock("initial_block", "initial_imei", gen_publicKey)
#  store_blocks.write("webi.fi.tech@gmail.com" + " " + "initial_block" + " " +"initial_imei" + " " + gen_publicKey + "\n")
#  gen_hash = gen_block.block_hash
#  # if the block for this user does not exist, create it. else, print values
#  currentHash = ""
#  if email not in all_blocks:
#  if last_block != []:
#  prev_block = NISCoinBlock(last_block[1], last_block[2], last_block[3])
#  prev_hash = prev_block.block_hash
#  else:
#  prev_hash = gen_hash
#  new_block = NISCoinBlock(prev_hash, imei, publicKey)
#  currentHash = new_block.block_hash
#  print("\n\n\nnew block details: \n", new_block.block_hash)
#  # store the newly created block
#  store_blocks.write(email + " " + prev_hash + " " + imei + " " + publicKey +"\n")
#  else:
#  print(all_blocks[email])
#  print("finished the initial process")
#  print("current hash is......", currentHash)
#  store_blocks.close()
#  data = {"currentHash": currentHash}
#  # return its hash
#  return jsonify(data)

# # ----------------------- SEARCH---------------------------
# @app.route("/searchPublicKey", methods=["GET"])
# def searchPublicKey():
#  # call getHash api
#  args = request.arg
#  decryptedHash = args['hash']
#  store_blocks = open("blocks.txt", "a+")
#  store_blocks.seek(0)
#  read_blocks = store_blocks.readlines()
#  all_blocks = dict()
#  for line in read_blocks:
#  curr = [x for x in line.strip().split()]
#  key = curr[0] #email
#  value = [curr[1], curr[2], curr[3]] #prev_hash, imei, publicKey
#  all_blocks[key] = value
#  retrievedPublicKey = ""
#  prevEmail = ""
#  for i in all_blocks:
#  if all_blocks[i][0] == decryptedHash:
#  retrievedPublicKey = all_blocks[prevEmail][2]
#  break
#  prevEmail = i
#  data = { "publicKey": retrievedPublicKey}
#  return jsonify(data)

class NISCoinBlock:
    def __init__(self, prev_hash, imei, publicKey):
        self.prev_hash = prev_hash
        self.imei = imei
        self.publicKey = publicKey
        # generating hash of the imei code
        self.block_hash = hashlib.sha256(self.imei.encode()).hexdigest()
@app.route("/getHash", methods=["GET"])
def getHash():
    args = request.args
    print(args) #for debugging
    email = args['email']
    imei = args['imei']
    publicKey = args['publicKey']
    print("DETAILS ARE........", email, imei, publicKey)
    # read already stored blocks
    store_blocks = open("blocks.txt", "a+")
    store_blocks.seek(0)
    all_blocks = dict()
    last_block = []
    read_blocks = store_blocks.readlines()
    for line in read_blocks:
        curr = [x for x in line.strip().split()]
        key = curr[0] #email
        value = [curr[1], curr[2], curr[3]] #prev_hash, imei, publicKey
        all_blocks[key] = value
        last_block = curr
    # create genesis block
    print(all_blocks)
    gen_hash = ""
    gen_publicKey ="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuJclDAJNt+JIbnSVSyp3kXP+JJzgo0DWoCm++tAROeM5jwAuoI8GWjuz0Vkz4krH4jrxYRnM6Hd2zeO6yQBzxk4JXSMccWqyEn9iShObKfL8B/QUYKZaduQ3KTwUzfWR8em0ePnLTfd2jXao417NeVSbNA/vKxZsK+jig+DJrPu5kJQwE18Idh7lX21wggLLVAGqXMVtNbsZXNiA3qF6lpRxNcgmGQ5Mx4ewSYv2Ledk7JuNDEJiGNiDxoa8qI3u2OPBkVrtOnc19/265f8Rapy1UsfzjP07P5/FZZxrSZSMr4XLOk6uwAP0UEWnPbeZp/Ps7WDWc6XdEn7pLjEbWwIDAQAB"
    gen_privateKey ="MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4lyUMAk234khudJVLKneRc/4knOCjQNagKb760BE54zmPAC6gjwZaO7PRWTPiSsfiOvFhGczod3bN47rJAHPGTgldIxxxarISf2JKE5sp8vwH9BRgplp25DcpPBTN9ZHx6bR4+ctN93aNdqjjXs15VJs0D+8rFmwr6OKD4Mms+7mQlDATXwh2HuVfbXCCAstUAapcxW01uxlc2IDeoXqWlHE1yCYZDkzHh7BJi/Yt52Tsm40MQmIY2IPGhryoje7Y48GRWu06dzX3/brl/xFqnLVSx/OM/Ts/n8VlnGtJlIyvhcs6Tq7AA/RQRac9t5mn8+ztYNZzpd0SfukuMRtbAgMBAAECggEBAI2QdPwJxDrTEsOLK3fzALIPaAgCPBFXx4IbofjOm3duuRTfieLe7XtEMDrMk4rn2PW6SKY0WD6sZ/Osw/IlI6Ug8fN42vZsYlbnVKUE9kmsrPcYjIw26Egn69n21unBfIUvu5XP1MhdkZEaQJnneeOkLEc4NS8xShI+z4FeYq0DLxEpkZzs+B7d0R6qRcuq1XkiI96iDbapnMXd/pFrYxSojBJxrY2LaBcOImKPqDmb0vqh6f30pSMuvfyR+S1ignpih3qwwxYxNdPGoMZJCW/d8i5+xd0x6P7DgRN0hAsQsW1a1Np5e4aAegIBMpxxvnGqHTHDoxiQAICcQkWbXRECgYEA39k7ThNEMnQH60+9g5jo5IIdF2BO3P48aghpV2ES8k+YxlQDEMkPd/jWQgCUaQ6s5znRO443wLn5dEpcSt6l38PLX/ONAzDMNC0f/s/4ORQH04F8uWuGYoNe0s1qyshWH0vSQpr9uHk9HsuLW9t+ajwMn21dvBlKDJe2o7/cC+kCgYEA0xpqegLCuD47q3j56kMk+Ap3pXySspVesOGAp924eqhCS0yKC6d8NR3K6n6ZtMsQjx2UT0hQHorFpgojyJlXprQhxOgCUP27jODaIs4qLKUVmkIJacuHguSFCYUpbyl5u4Ref4OFEU/4ZTyhIT9pxucQglhGMGGGSwjAkMNjlqMCgYEA2L9dP1JEfJ4BdQY3OQ98opaiWJo2gqHiGcGfTq5+TAZqpc9/UGd/BOn7fNlW2wsMvLAtOv+QWJs7QjEmgJBqCOtrJ7OKXQaJFBSFoJP7hDkzAsek312QOB+AV5nzx/qH+bHPHBM7jb5HQmRQwlccZv1SM6UQWCwcmWjlvlTuWtECgYAvMVmaWyGixK7cP5hHKamLFfP3d+jnqYLYsiDr5iJGsXTYlozJ3DBlQ3rIf3LnOvpBtFAihTz8BvP2kY+8WaOBrgVamq9h4cda0C2T2FkPT/yLVrX6A7kQpvuizDUeF7ySEh56DTHjU+ho4Wv4HdAM2j0Tlp5iVHsMLTG3aybJVwKBgHyLIrvIqFmkAyrjOTQVfRgdnck8UE8hT0wY3K2A1bXFtgfmKp4vMsT7/KHNZZOCgN95BF1xs2VrSVAa9TBJzv3viqqTjUJwiKa9zNgjr166b8QkFZI0urDHn19owMiJ3fR1qyazESHGZSEv7VYNX/yiJL+PmO57GRlC2buAgeAb"
    if last_block == []:
        # create genesis block
        print("creating first block...")
        gen_block = NISCoinBlock("initial_block", "initial_imei", gen_publicKey)
        store_blocks.write("webi.fi.tech@gmail.com" + " " + "initial_block" + " " +"initial_imei" + " " + gen_publicKey + "\n")
        gen_hash = gen_block.block_hash
    # if the block for this user does not exist, create it. else, print values
    currentHash = ""
    if email not in all_blocks:
        if last_block != []:
            prev_block = NISCoinBlock(last_block[1], last_block[2], last_block[3])
            prev_hash = prev_block.block_hash
        else:
            prev_hash = gen_hash
        new_block = NISCoinBlock(prev_hash, imei, publicKey)
        currentHash = new_block.block_hash
        print("\n\n\nnew block details: \n", new_block.block_hash)
        # store the newly created block
        store_blocks.write(email + " " + prev_hash + " " + imei + " " + publicKey +"\n")
    else:
        print(all_blocks[email])
    print("finished the initial process")
    print("current hash is......", currentHash)
    store_blocks.close()
    data = {"currentHash": currentHash}
    # return its hash
    return jsonify(data)

# ----------------------- SEARCH---------------------------
@app.route("/searchPublicKey", methods=["GET"])
def searchPublicKey():
    # call getHash api
    args = request.arg
    decryptedHash = args['hash']
    store_blocks = open("blocks.txt", "a+")
    store_blocks.seek(0)
    read_blocks = store_blocks.readlines()
    all_blocks = dict()
    for line in read_blocks:
        curr = [x for x in line.strip().split()]
        key = curr[0] #email
        value = [curr[1], curr[2], curr[3]] #prev_hash, imei, publicKey
        all_blocks[key] = value
    retrievedPublicKey = ""
    prevEmail = ""
    for i in all_blocks:
        if all_blocks[i][0] == decryptedHash:
            retrievedPublicKey = all_blocks[prevEmail][2]
            break
        prevEmail = i
    data = { "publicKey": retrievedPublicKey}
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
