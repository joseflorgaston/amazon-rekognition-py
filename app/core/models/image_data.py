class ImageData:
    def __init__(self, parking_spot_id, camera_id, labeled_image_url, original_image_url, free_spaces, occupied_spaces, date):
        self.parking_spot_id = parking_spot_id
        self.camera_id = camera_id
        self.labeled_image_url = labeled_image_url
        self.original_image_url = original_image_url
        self.free_spaces = free_spaces
        self.occupied_spaces = occupied_spaces
        self.date = date
