from bson import ObjectId

class Review:
    """
    Represents a user review for a film.
    """

    def __init__(self, film_id, profile_id, text, review_id=None):
        """
        Initializes a Review instance.

        Args:
            film_id (str): The unique MongoDB ObjectId of the film.
            profile_id (str): The unique MongoDB ObjectId of the profile who wrote the review.
            text (str): The review text.
            review_id (str, optional): The unique ID of the review (MongoDB _id).
        """
        self.review_id = str(review_id) if review_id else None
        self.film_id = str(film_id)
        self.profile_id = str(profile_id)
        self.text = text

    def to_dict(self):
        """
        Converts the Review instance into a dictionary.
        """
        return {
            "_id": self.review_id,
            "film_id": self.film_id,
            "profile_id": self.profile_id,
            "text": self.text
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Review instance from a dictionary.
        """
        return Review(
            review_id=data.get("_id"),
            film_id=data.get("film_id"),
            profile_id=data.get("profile_id"),
            text=data.get("text")
        )
