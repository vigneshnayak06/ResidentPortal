from configs.config import Config


class ProductionConfig(Config):
    DB_NAME = "dynamodb"
    SNS = "sns"
    AWS_ACCESS_KEY_ID = "ASIAWOYNGN4BCN3G53TL"
    AWS_SECRET_ACCESS_KEY = "D6KaqMKTACXJb0gw9oJV0pyj72TX6sLPoxEo71G/"
    AWS_SESSION_TOKEN = "FwoGZXIvYXdzEBQaDMa2nTfPDH4xrdZ4ACLAAZuCBdcWKr4tydlQV/r+xHDnscZAKyiwmyOHFpn7JMOuy+mzmbjlh+pnXycWwSAwmOTibevY4yrYLPJHmnQyp51ITAXHbSm6UBZ+HmJ43ogOcSIwDlt/OogcjStMUKgIS3bJIeF8DK/tMRnSWd5TRkJF3VG7WRTDchXmyGBDG7qN+0Gj5VCLrK19pH/e8/033mgoy7Tj+fPNx35ZEl0YSMFdjSX4QjlL9xyJjbLVBNiIzjqG6j4RPK/bay3xgQuaJCjw/7OSBjItZSm/8MPHxR5A8iZXn0FBTst5LLqGOxTyhB2E2Yi2lFY8BEFO2M7+6nXvQA/s"
    AWS_REGION = "us-east-1"
    AWS_SESSION = ""
    BUCKET_NAME = "servicerequestimage"
    COGNITO_CLIENT_ID = "2g2bbfsshtrt34fsp15sacir1r"
    AUTH_FLOW = "USER_PASSWORD_AUTH"

