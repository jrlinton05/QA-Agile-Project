class Review:
    def __init__(self, review_id, review_title, review_body, review_score, username, product_id):
        self.review_id = review_id
        self.review_title = review_title
        self.review_body = review_body
        self.review_score = review_score
        self.username = username
        self.product_id = product_id

    def to_dict(self):
        return {
            "review_id": self.review_id,
            "review_title": self.review_title,
            "review_body": self.review_body,
            "review_score": self.review_score,
            "username": self.username,
            "product_id": self.product_id
        }