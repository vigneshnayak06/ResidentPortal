from flask import current_app

from vendors.helper import Helper


class DynamoDB:

    def __init__(self):
        self.session = Helper.get_session()
        self.resource = self.get_dynamodb_resource()

    def get_dynamodb_resource(self):
        db = current_app.config["DB_NAME"]
        resource = self.session.resource(db, region_name=current_app.config["AWS_REGION"])
        return resource

    def insert(self, table_name, data):
        table_res = self.resource.Table(table_name)
        response = table_res.put_item(
            Item=data
        )
        return response

    def delete(self, table_name, id, key_column):
        table_res = self.resource.Table(table_name)
        response = table_res.delete_item(
            Key={
                key_column: id
            }
        )
        return response

    def update(self, table_name, id, data, key_column):
        table_res = self.resource.Table(table_name)
        update_expression = "SET"
        expression_attribute_values = dict()
        for key, value in data.items():
            update_expression += f' {key}=:{key},'
            expression_attribute_values[f':{key}'] = value
        update_expression = update_expression.rstrip(",")
        response = table_res.update_item(
            Key={
                key_column: id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def get_record(self, table_name, key_value_dict):
        print(key_value_dict)
        table_res = self.resource.Table(table_name)
        response = table_res.get_item(
            Key=key_value_dict
        )
        return [response['Item']]

    def get_all_records(self, table_name):
        table_res = self.resource.Table(table_name)
        response = table_res.scan()
        return response['Items']

