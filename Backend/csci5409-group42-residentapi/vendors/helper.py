import boto3
from flask import current_app


class Helper:
    @staticmethod
    def get_session():
        session = current_app.config["AWS_SESSION"]
        if not session:
            access_key = current_app.config["AWS_ACCESS_KEY_ID"]
            secret_key = current_app.config["AWS_SECRET_ACCESS_KEY"]
            session_token = current_app.config["AWS_SESSION_TOKEN"]
            region_name = current_app.config["AWS_REGION"]
            session = boto3.Session(aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key,
                                    aws_session_token=session_token,
                                    region_name=region_name)
            current_app.config["AWS_SESSION"] = session
        return session
