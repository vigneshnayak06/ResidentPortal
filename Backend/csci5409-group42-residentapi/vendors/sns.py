from botocore.exceptions import ClientError
from flask import current_app
from vendors.helper import Helper

class SNS:

    def __init__(self):
        self.session = Helper.get_session()
        self.resource = self.get_sns_resource()

    def get_sns_resource(self):
        sns = current_app.config["SNS"]
        resource = self.session.resource(sns, region_name=current_app.config["AWS_REGION"])
        return resource

    def publish_notification(self, topic_arn, message, subject):
        topic = self.resource.Topic(topic_arn)
        response = topic.publish(Message=message, Subject=subject)
        return response

    def create_new_topic(self, topic_name):
        topic = self.resource.create_topic(Name=topic_name)
        return topic

    def subscribe_to_topic(self, topic_name, protocol, endpoint):
        """

        :param topic_name: topic to subscribe to
        :param protocol: 'email' / 'sms'
        :param endpoint: email_id / phone_number
        :return: subscription
        """
        subscription = topic_name.subscribe(Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
        return subscription

    def publish_text_message(self, phone_number, message):
        try:
            response = self.resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
        except ClientError:
            raise
        else:
            return message_id







