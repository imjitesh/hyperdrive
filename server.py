from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth
import json, string, sqlite3, re, os
import urlparse

from random import randint

def pre_data_container(title):
	return """<!DOCTYPE html><html lang="en"> <head> <title>"""+title+"""</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> <script src='static/js/jquery-sortable-min.js'></script> <style type="text/css"> body.dragging, body.dragging *{cursor: move !important;}.dragged{position: absolute; opacity: 0.5; z-index: 2000;}ol.example li.placeholder{position: relative;}ol.example li.placeholder:before{position: absolute;}textarea{margin:0px; padding:0px; color:#000; display: block; opacity:1; background:#ffffff; border:0; width:100%; resize:none;}.title-area{margin-top:40px; font-size:36px; line-height:36px; height:40px; font-weight:500;}.subtitle-area{margin-top:0px; font-size:24px; font-weight:300;}.heading-area{margin-top:0px; margin-bottom:10px; font-size:24px; line-height:24px; height:27px; font-weight:500;}.text-area{margin-top:0px; font-size:18px; font-weight:400;}::placeholder{opacity:0.6;}.add_icons{border:1px solid #000;padding:5px;border-radius:10px;margin-right: 10px;opacity:0.7;cursor:pointer; display:none;}textarea, select, input, button{outline: none;}</style> </head> <body> <div class="row" style="margin:0;margin-bottom:50px;"> <div class="col-sm-12" style="position:fixed; background-color:#0050ff;color:#FFFFFF;height:50px;z-index:9;"> <button type="button" class="btn btn-info minimap bt-md disabled" style="float:right;margin-top:8px;margin-left:20px;">Minimap</button> <button type="button" class="btn btn-success btn-md save" style="float:right;margin-top:8px;margin-left:20px;">Save</button> <button type="button" class="btn btn-info btn-md publish" style="float:right;margin-top:8px;">Publish</button> </div></div><div class="container-fluid data-container" style="margin:0 auto;width:75%;">"""

post_data_container = """</div><div class="container-fluid" style="margin:0 auto;width:75%;"> <div class="row" style="margin-bottom:100px;"> <div class="col-sm-12" style="background-color:#ffffff;color:#000000;"> <img class="add_data_button" src="static/img/plus.png" width="36" style="margin-right:10px;cursor:pointer;"/> <img class="add_icons type1" src="static/img/type1.png" width="70"/> <img class="add_icons type2" src="static/img/type2.png" width="100"/> <img class="add_icons type3" src="static/img/type3.png" width="40"/> <img class="add_icons type4" src="static/img/type4.png" width="38"/> <img class="add_icons type5" src="static/img/type5.png" width="70"/> </div></div></div><div class="type1-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-8" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type2-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-4" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div><div class="col-sm-4" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type3-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-12" style=""> <textarea class="heading-area" placeholder="Add heading here."></textarea> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type4-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-12" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div></div></div><div class="type5-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-8" style=""> <img src="static/img/compare_image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div id="myModal" class="modal fade" role="dialog"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal">&times;</button> <h4 class="modal-title">Image URL Editor</h4> </div><div class="modal-body"> <div class="form-group"> <label for="image_url">Image URL</label> <input type="url" class="form-control" id="image_url"> </div></div><div class="modal-footer"> <button type="button" class="btn btn-success update-image" data-dismiss="modal">Update</button> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> </div></div></div></div><script type="text/javascript" src="static/js/required.js"></script> </body></html>"""

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
	ofile.write(pre_data_container(title)+urlparse.unquote(row_data)+post_data_container)
	ofile.close()
	return "Successfully saved"

if __name__ == '__main__':
    app.run()