class Review:
    def __init__(self, review_title, review_body, review_score, username):
        self.review_title = review_title
        self.review_body = review_body
        self.review_score = review_score
        self.username = username

    def to_dict(self):
        return {
            "review_title": self.review_title,
            "review_body": self.review_body,
            "review_score": self.review_score,
            "username": self.username
        }