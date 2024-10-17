from flask import Flask, render_template, session, redirect, request, send_file
from flask_session import Session

from login_handler import LoginHandler
from mongo_interface import MongoInterface
from encryption_interface import EncryptionInterface
from blob_interface import BlobInterface

from io import BytesIO

import hashlib

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/')
def default_route():
    if not session.get('user'):
        return redirect('/login')
    else:
        return render_template('homepage.html', error = None)
    
@app.route('/login', methods=["POST", "GET"])
def login_route():
    if request.method == "POST":
        login_handler = LoginHandler()
        login_response = login_handler.login(request.form.get('username'), request.form.get('password'))

        if login_response == True:
            session['user'] = request.form.get('username')
            return redirect('/')
        else:
            return render_template('login.html', error = 'Invalid login')
    else:
        if not session.get('user'):
            return render_template('login.html', error = None)
        else:
            return redirect('/')
        
@app.route('/search', methods=["POST"])
def search_route():
    data = request.form.get("filename")

    if not data:
        return render_template('homepage.html', error = 'Cannot have empty filename for search')
    else:
        mongo_client = MongoInterface()

        res = mongo_client.find_evidence_for_file(data)

        return render_template('files_result.html', files = res)
    
@app.route('/getevidence', methods=["POST"])
def get_evidence():
    e_f_name = request.form.get("evidence_name")

    if not e_f_name:
        print('todo error handling')
    else:
        encryption = EncryptionInterface()
        blob = BlobInterface()
        mongo = MongoInterface()

        name = encryption.decrypt_file_name(e_f_name)
        content_blob = blob.get_content_file(name)
        decrypted_contents = encryption.decrypt_content(content_blob.decode('utf-8'))

        curr_hash = hashlib.md5(decrypted_contents).hexdigest()
        stored_hash = mongo.get_stored_plain_hash(e_f_name)

        if curr_hash == stored_hash:
            return send_file(BytesIO(decrypted_contents), download_name = e_f_name)
        else:
            print("===============================================")
            print(curr_hash)
            print("===============================================")
            print(stored_hash)
            print("===============================================")
            return None