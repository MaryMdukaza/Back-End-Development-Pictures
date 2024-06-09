from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################

def load_pictures():
    json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'pictures.json')
    with open(json_file_path, 'r') as file:
        return json.load(file)

pictures = load_pictures()

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(pictures)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in pictures if pic['id'] == id), None)
    if picture is None:
        return jsonify({"error": "Picture not found"}), 404   
    return jsonify(picture)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/", methods=["POST"])
def create_picture():
    pictureData = request.json
    for picture in pictures:
        if picture['id'] == pictureData['id']:
            return ({"Message": f"Picture with id {pictureData['id']} already present"}, 302)
    pictures.append(pictureData)
    json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'pictures.json')
    with open(json_file_path, 'w') as file:
        json.dump(pictures, file, indent=4)
    return ({"Message": "Picture added successfully"}, 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
