from vendors.dynamodb import DynamoDB

class Resident:
    def __init__(self):
        self.TABLE_NAME = "user"
        self.primary_key = "user_id"
        self.dynamo = DynamoDB()

    def get_all_residents(self):
        return self.dynamo.get_all_records(self.TABLE_NAME)

    def insert_resident(self, data):
        return self.dynamo.insert(self.TABLE_NAME, data)

    def delete_service_request(self, id):
        response = self.dynamo.delete(self.TABLE_NAME, id, self.primary_key)
        return response

    def update_resident(self, user_id, data):
        return self.dynamo.update(self.TABLE_NAME, user_id, data, self.primary_key)

    def resident_doesnot_exist(self, new_resident):
        residents = self.get_all_residents()
        for resident in residents:
            if resident["user_email"] == new_resident["user_email"]:
                return "0"

        return "1"