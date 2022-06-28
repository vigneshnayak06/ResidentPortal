from vendors.dynamodb import DynamoDB
from vendors.s3 import S3
from entities.resident import Resident


class ServiceRequest:
    def __init__(self):
        self.TABLE_NAME = "request"
        self.primary_key = "request_id"
        self.dynamo = DynamoDB()
        self.s3 = S3()

    def get_all_requests(self):
        return self.dynamo.get_all_records(self.TABLE_NAME)

    def get_user_requests(self, user_id):
        all_requests = self.dynamo.get_all_records(self.TABLE_NAME)
        filtered_requests = [request for request in all_requests if request["user_id"] == user_id]
        return filtered_requests

    def insert_service_request(self, data, image):
        if image:
            # place image in s3 and store url in dynamodb
            data["request_image"] = self.place_file_in_s3(data['request_id'], image)
        return self.dynamo.insert(self.TABLE_NAME, data)

    def delete_service_request(self, id):
        response = self.dynamo.delete(self.TABLE_NAME, id, self.primary_key)
        return response

    def update_service_request(self, request_id, data, image):
        if image:
            # place image in s3 and store url in dynamodb
            data["request_image"] = self.place_file_in_s3(request_id, image)
        return self.dynamo.update(self.TABLE_NAME, request_id, data, self.primary_key)

    def place_file_in_s3(self, request_id, image):
        key = f"request-images/{request_id}/{image.filename.replace(' ', '_')}"
        image_url = self.s3.store_file(key, image)
        return image_url

    def get_all_requests_for_admin(self):
        requests = self.get_all_requests()          #user_id
        resident_obj = Resident()
        residents = resident_obj.get_all_residents()        #user_id

        combined_data = []
        for resident in residents:
            user_id = resident["user_id"]
            filtered_requests = [request for request in requests if request["user_id"] == user_id]
            for fil_request in filtered_requests:
                fil_request["user_uno"] = resident["user_uno"]
                fil_request["user_firstname"] = resident["user_firstname"]
                combined_data.append(fil_request)

        return combined_data


