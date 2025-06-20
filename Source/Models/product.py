from Source.Helpers.count_number_of_reviews import count_number_of_reviews
from Source.Helpers.get_average_review_score import get_average_review_score


class Product:
    def __init__(self, product_id, name, image_url):
        self.product_id = product_id
        self.name = name
        self.image_url = image_url
        self.num_reviews = self.generate_num_reviews()
        self.average_score = self.generate_average_score()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "image_url": self.image_url,
            "num_reviews": self.num_reviews,
            "average_score": self.average_score
        }

    def generate_num_reviews(self):
        return count_number_of_reviews(self.product_id)

    def generate_average_score(self):
        return get_average_review_score(self.product_id)