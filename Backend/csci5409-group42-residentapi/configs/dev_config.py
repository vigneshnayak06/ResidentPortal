from configs.config import Config


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "dynamodb"
    SNS = "sns"
    AWS_ACCESS_KEY_ID = "ASIAWOYNGN4BDEZP7ZOX"
    AWS_SECRET_ACCESS_KEY = "hxqTvwXJqki32YEPZH571cDPlkxAV6ktqPHgXWmz"
    AWS_SESSION_TOKEN = "FwoGZXIvYXdzEOT//////////wEaDGhLc9NGJ/Sr9kjeQyLAAaYWs2SU1hJvGiHdFXZjM5OyI0NrSZBWUqqNQ/UNDsyoJIceRajgkeWSlbTXdK+SgvyJxikKwQ7OzhboAE/HbcoWbJ0j5TBhMIUc5IZXJNTOlk1P/+QgM2KvRllgoOEFwi/u97TKLVq9x0Z40FH6h4UVSnPhJadRAiM7PNFl8+1ugEI/7pIyzwrtQ2VYcIdmotI1rIehpLwMKtRupUZiKXdE8APTP4n9dhAeLyCaFkgmbukzTD/vuNcqKIq9Q50/yyimp6mSBjItG49mb+G4MCs1Pk/1I7GprBcu5F4+4RSCgrolaFBIEe08doSXynGenil8DI8Z"
    AWS_REGION = "us-east-1"
    AWS_SESSION = ""
    BUCKET_NAME = "servicerequestimage"
    COGNITO_CLIENT_ID = "2g2bbfsshtrt34fsp15sacir1r"
    AUTH_FLOW = "USER_PASSWORD_AUTH"
