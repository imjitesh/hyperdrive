from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth
import json, string, sqlite3, re, os
import urlparse

from random import randint

def pre_data_container(title):
	return """<!DOCTYPE html><html lang="en"><head><title>"""+title+"""</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <link rel="stylesheet" href="static/css/required.css"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> </head> <script type="text/javascript" src="static/js/image_comparison.js"></script> <body> <div class="container-fluid" style="margin:0 auto;width:100%;background-color:#0050ff;"> <div class="row" style="margin:0;width:100%"> <div class="col-sm-10" style="color:#FFFFFF;z-index:9;line-height:60px;"> <h3 style="margin-top:15px;font-weight:300;">Modular Instructions </h3> </div><div class="col-sm-1" style="color:#FFFFFF;height:60px;z-index:9;line-height:60px;"> <button type="button" class="btn btn-success btn-md save" style="">Save</button> </div><div class="col-sm-1" style="color:#FFFFFF;height:60px;z-index:9;line-height:60px;"> <button type="button" class="btn btn-info btn-md publish" style="">Publish</button> </div></div></div><div class="container-fluid data-container" style="margin:0 auto;width:75%;">"""

post_data_container = """</div><div class="container-fluid" style="margin:0 auto;width:75%;"> <div class="row" style="margin-bottom:100px;"> <div class="col-sm-12" style="background-color:#ffffff;color:#000000;"> <img class="add_data_button" src="static/img/plus.png" width="36" style="margin-right:10px;cursor:pointer;"/> <img class="add_icons type1" src="static/img/type1.png" width="70"/> <img class="add_icons type2" src="static/img/type2.png" width="100"/> <img class="add_icons type3" src="static/img/type3.png" width="40"/> <img class="add_icons type4" src="static/img/type4.png" width="38"/> <img class="add_icons type5" src="static/img/type5.png" width="70"/> </div></div></div><div class="type1-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-8" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type2-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-4" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div><div class="col-sm-4" style=""> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type3-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-12" style=""> <textarea class="heading-area" placeholder="Add heading here."></textarea> <img class="img-show" src="static/img/image_placeholder.png" width="100%" height="100%" data-toggle="modal" data-target="#myModal"> </div></div></div><div class="type4-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-12" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div></div></div><div class="type5-container" style="display:none;"> <div class="row data-row" style="margin-bottom:60px;"> <div class="col-sm-4" style="background-color:#ffffff;color:#000000;"> <textarea class="heading-area" placeholder="Add heading here."></textarea> <textarea class="text-area" placeholder="Add text here."></textarea> </div><div class="col-sm-8" style=""> <div class="ba-slider"> <img class="img-show" src="static/img/compare_image_placeholder1.png" data-toggle="modal" data-target="#myModal" alt=""> <div class="resize"> <img class="img-show" src="static/img/compare_image_placeholder2.png" data-toggle="modal" data-target="#myModal" alt=""> </div><span class="handle"></span> </div></div></div></div><div id="myModal" class="modal fade" role="dialog"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal">&times;</button> <h4 class="modal-title">Image URL Editor</h4> </div><div class="modal-body"> <div class="form-group"> <label for="image_url">Image URL</label> <input type="url" class="form-control" id="image_url"> </div></div><div class="modal-footer"> <button type="button" class="btn btn-success update-image" data-dismiss="modal">Update</button> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> </div></div></div></div><script type="text/javascript" src="static/js/required.js"></script> </body></html>"""

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():	
	return render_template('index.html')

@app.route('/<int:id>')
def draft(id):
	#return render_template('index.html')
	return render_template(str(id)+".html")

@app.route('/save', methods=['POST'])
def save():
	newFile = randint(999,999999999)
	row_data = request.files['html_file']
	fileName = str(newFile) if row_data.filename == '1' else row_data.filename
	row_data.save("templates/"+fileName+".html")
	ifile = open("templates/"+fileName+".html", 'rb')
	html_data = ifile.read()
	ifile.close()
	ofile = open("templates/"+fileName+".html","wb")
	ofile.write("<!DOCTYPE html>"+html_data)
	ofile.close()

	return json.dumps({'_id':fileName,"is_created":row_data.filename == '1'})

if __name__ == '__main__':
    app.run()