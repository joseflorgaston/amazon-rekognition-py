class S3ImageData:
    def __init__(self, image_data, bucket_name, file_name, max_results):
        self.image_data = image_data
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.max_results = max_results
