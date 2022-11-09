import json
from turtle import pu
from flask import Flask, redirect, url_for, render_template, jsonify, request, send_file,session
import hashlib
from flask_ngrok import run_with_ngrok
from rsa import PublicKey
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
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import rsa
app = Flask(__name__)
run_with_ngrok(app)
# ------------- creating block ------------------
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
@app.route("/", methods=["GET", "POST"])
def home():
    return jsonify("hello")
if __name__ == "__main__":
    app.run()