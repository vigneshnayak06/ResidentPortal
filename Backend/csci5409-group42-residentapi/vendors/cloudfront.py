class CloudFront:
    def __init__(self):
        self.cloudfront_domain = "https://da7a0tunnnyvb.cloudfront.net/"

    def get_cloudfront_url(self, s3_key):
        return f"{self.cloudfront_domain}{s3_key}"