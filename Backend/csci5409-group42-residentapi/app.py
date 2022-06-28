import uuid
from crypt import methods
import boto3
from flask import Flask, request, json, jsonify
from boto3.dynamodb.conditions import Key
from entities.service_request import ServiceRequest
from entities.resident import Resident
from services.user_auth_service import UserAuth
from entities.sns_operation import SNSOperation
from flask_cors import CORS

import logging

app = Flask(__name__)
CORS(app)

if app.config["ENV"] == "production":
    app.config.from_object("configs.prod_config.ProductionConfig")
else:
    app.config.from_object("configs.dev_config.DevelopmentConfig")  # add config values in configs folder and
    # retrieve anywhere in the project using app.config("key")


@app.route("/")
def init_test():
    return "<h2>Welcome to Resident Service Portal.</h2><h3>Application is running.</h3>"


@app.route("/user/authentication", methods=['POST', 'GET'])
def index():
    json_input = request.json
    username = json_input['user_email']
    password = json_input['user_password']
    user_auth = UserAuth()
    admin_result = user_auth.check_if_admin(username, password)
    if admin_result != "Admin":
        record = user_auth.scan_db_for_user(username, password)
        if record:
            user = record[0]
            return jsonify(success=True, user_type="Resident", user_id=str(user["user_id"]))
        else:
            return jsonify(success=False, data="Invalid Username and Password")
    else:
        return jsonify(success=True, user_type="Admin")


@app.route("/service-requests", methods=['POST'])
def get_all_service_requests():
    try:
        js_data = request.get_json()
        user_id = js_data["ID"]
        service_request = ServiceRequest()
        requests = service_request.get_user_requests(user_id)
        response = {
            'data': requests,
        }

        return jsonify(response)
    except Exception as e:
        logging.log(e.args)
        return "Exception occurred", 500


@app.route("/admin/service-requests", methods=['GET'])
def get_requests_for_admin():
    try:
        service_request = ServiceRequest()
        requests = service_request.get_all_requests_for_admin()
        response = {
            'data': requests,
        }

        return jsonify(response)
    except Exception as e:
        logging.log(e.args)
        return "Exception occurred", 500


@app.route("/upsert-service-request", methods=['POST'])
def store_service_request():
    json_data = request.form
    request_id = json_data["request_id"]  # if 0 insert, else update
    request_category = json_data["request_category"]
    request_title = json_data["request_title"]
    request_description = json_data["request_description"]
    user_id = json_data["user_id"]
    request_status = json_data["request_status"]
    request_image = request.files["request_image"] if "request_image" in request.files.keys() else None

    try:
        service_request = ServiceRequest()
        data = {
            "user_id": user_id,
            "request_category": request_category,
            "request_title": request_title,
            "request_description": request_description,
            "request_status": request_status
        }

        sns = SNSOperation()

        if request_id == '0':
            data["request_id"] = str(uuid.uuid4())
            service_request.insert_service_request(data, request_image)
            sns.publish_notification(
                f"Hi! You have a new service request: \n Request ID: {data['request_id']} \n Request Category: {request_category} \n Request Title: {request_title}",
                f"New Service Request from {user_id}")
        else:
            service_request.update_service_request(request_id, data, request_image)
            sns.publish_notification(
                f"Hi! Service request updated: \n Request ID: {request_id} \n Request Title: {request_title}",
                f"New Service Request from {user_id}")

        return str(1), 200

    except Exception as e:
        logging.log(e.args)
        return "Exception occured", 500


@app.route("/requests/update-status", methods=['POST'])
def update_request_status():
    json_input = request.get_json()
    request_id = json_input['request_id']
    request_status = json_input['request_status']
    try:
        service_request = ServiceRequest()
        data = {
            "request_status": request_status
        }
        service_request.update_service_request(request_id, data, None)

        return str(1), 200

    except Exception as e:
        logging.log(e.args)
        return "Exception occured", 500


@app.route("/delete-request", methods=['DELETE'])
def delete_request():
    try:
        json_input = request.get_json()
        request_id = json_input['ID']
        service_request = ServiceRequest()
        service_request.delete_service_request(request_id)
        sns = SNSOperation()
        sns.publish_notification(
            f"Hi! A service request {id} has been deleted.",
            f"Service request deleted")
        return "1", 200
    except Exception as e:
        return {
            'msg': 'Some error occured',
            'trace': e.with_traceback()
        }


@app.route("/users", methods=['GET'])
def get_all_users():
    try:
        resident_obj = Resident()
        residents = resident_obj.get_all_residents()
        response = {
            'data': residents,
        }

        return jsonify(response)
    except Exception as e:
        logging.log(e.args)
        return "Exception occurred", 500


@app.route("/upsert-resident", methods=['POST'])
def store_resident():
    json_data = request.form
    u_id = json_data["Id"]  # if 0 insert, else update
    fname = json_data["fname"]
    lname = json_data["lname"]
    email = json_data["email"]
    uno = json_data["uno"]
    spass = json_data["spass"]
    phone_number = json_data["phone_number"]

    try:
        resident_obj = Resident()
        data = {
            "user_firstname": fname,
            "user_lastname": lname,
            "user_email": email,
            "user_uno": uno,
            "user_password": spass,
            "phone_number" : phone_number
        }

        if u_id == '0':
            data["user_id"] = str(uuid.uuid4())
            resident_obj.insert_resident(data)
            sns = SNSOperation()
            sns.publish_text_message("+1"+phone_number, f"Welcome to Resident Service Portal. Please find your login details for the website. \n Email: {email} \n Password: {spass}")
        else:
            resident_obj.update_resident(u_id, data)

        return str(1), 200

    except Exception as e:
        logging.log(e.args)
        return "Exception occured", 500


@app.route("/check-resident", methods=["POST"])
def check_if_resident_exists():
    """
    :return: 1 if resident is new and does not exist in the database
    """
    try:
        json_data = request.form
        data = {
            "user_email": json_data["email"]
        }
        resident_obj = Resident()
        return resident_obj.resident_doesnot_exist(data)
    except Exception as e:
        logging.log(e.args)
        return "Exception occurred", 500


@app.route("/delete-resident", methods=['DELETE'])
def delete_resident():
    try:
        json_input = request.get_json()
        user_id = json_input['ID']
        resident_obj = Resident()
        resident_obj.delete_service_request(user_id)
        return "1", 200
    except Exception as e:
        return {
            'msg': 'Some error occured',
            'trace': e.with_traceback()
        }


if __name__ == "__main__":
    app.run(debug=True, port=5556)
