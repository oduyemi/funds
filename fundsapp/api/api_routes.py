from flask import jsonify, request, make_response,json
from . import apiobj
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import delete
from fundsapp.models import db, B_user, Business

auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     deets = db.session.query(Merchant.mer_pwd).filter(Merchant.mer_username==username).first()
#     if deets:
#         return deets.mer_pwd
#     return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({"status":False, "message": "Unauthorized access"}), 401)

# @apiobj.route("/createnew", methods=["POST"])
# @auth.login_required
# def create_new():
#     #{"name":"2B/R", "price":'2000000', "contact":'Ade', "cat":"1","filename":"http//127.0.0.5000/static/assets/images/1.png"}
#     if request.is_json:
#         data = request.get_json() # will extract the json from the request and allow us to manipulate it as a python dictionary
#         name = data.get("name")
#         price = data.get("price")
#         contact = data.get("contact")
#         cat = data.get('cat')
#         file = data.get('filename')
#         #instantiate an object of property
#         if name !=  None and price != None and contact != None and cat != None and file != None:
#             p = Property(prop_name = name, prop_price = price, prop_contact = contact, property_cat = cat, prop_filename = file)
#             db.session.add(p)
#             db.session.commit()
#             return "Property Added!"
#         else:
#             return ("Please specify JSON in the correct format")

#     else:
#         return "Please supply data in JSON format"

# @apiobj.route("/listall", methods=["GET"])
# def list_all():
#     props = Property.query.join(Category).add_columns(Category).all()
#     if props:
#         record = [] #[{},{},{},{}]
#         for p, c in props:
#             a = {}
#             a["name"] = p.prop_name
#             a["contact"] = p.prop_contact
#             a['category'] = c.cat_name
#             a['price'] = p.prop_price
#             a['filename'] = p.prop_filename
#             record.append(a)
#         data2send = {"status":True, "message":record}
#     else:
#         data2send = {"status":False, "message":"No Property Found!"}
#     return jsonify(data2send)


# @apiobj.route("/listone/<id>", methods=["GET"])
# def list_one(id):
#     data = db.session.query(Property, Category).join(Category).filter(Property.prop_id==id).first()
#     if data:
#         #(<Property,Category>)
#         propertyname = data[0].prop_name
#         propertycat = data[1].cat_name
#         propertyprice = data[0].prop_price
#         propertyimg = data[0].prop_filename
#         propertycontact = data[0].prop_contact
#         # Save within a python dictionary, convert to json and return
#         deets = {"name":propertyname, "price":propertyprice, "cat":propertycat, "img":propertyimg, "contact": propertycontact}
#         data2send = {"status": True, "message":deets}
#     else:
#         data2send = {"status":False, "message": "invalid Parameter Detected"}
#     rsp = make_response(json.dumps(data2send),200)
#     rsp.headers["Content-type"] = "application/json"
#     return rsp

# @apiobj.route("/update/<id>", methods=["PUT"])
# def update_property(id):
#     return "Hostel Updated"

# @apiobj.route("/delete/<id>", methods=["DELETE"])
# def delete_property(id):
#     query = db.session.execute(delete(Property).where(Property.prop_id==id))
#     db.session.commit()
#     return "Property Deleted!"