from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth
import json, string, sqlite3, re, os,urllib2

from random import randint

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	newFile = randint(999,999999999)
	ifile = open("templates/index.html", "rb")
	ofile = open("templates/"+str(newFile)+".html","wb")
	ofile.write(ifile.read())
	ifile.close()
	ofile.close()
	#return render_template('index.html')
	return redirect('/'+str(newFile))

@app.route('/<int:id>')
def draft(id):
	#return render_template('index.html')
	return render_template(str(id)+".html")

@app.route('/save', methods=['GET', 'POST'])
def publish():
	row_data = request.args.get('row_data').encode('utf-8')
	_id = request.args.get('_id')
	ofile = open("templates/"+str(_id)+".html","wb")
	ofile.write("<!DOCTYPE html><html lang='en'>"+urllib2.unquote(row_data)+"</html>")
	ofile.close()
	return "Successfully saved"

if __name__ == '__main__':
    app.run()