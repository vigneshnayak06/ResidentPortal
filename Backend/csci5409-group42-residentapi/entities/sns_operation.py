from vendors import sns
from vendors.sns import SNS

class SNSOperation:

    def __init__(self):
        self.TOPIC_ARN = "arn:aws:sns:us-east-1:444019928834:admin-notifier"
        self.sns = SNS()

    def publish_notification(self, message, subject):
        return self.sns.publish_notification(self.TOPIC_ARN, message, subject)

    def publish_text_message(self, phone_number, message):
        return self.sns.publish_text_message(phone_number,message)