class Film:
    """
    Represents a film with its details, including title, cast, release year, genre, and rating.

    Attributes:
        title (str): Title of the film.
        actors (list): A list of actor surnames.
        release_year (int): Year the film was released.
        genre (str): Genre of the film (e.g., 'Drama', 'Action').
        rating (float): Rating of the film (e.g., IMDb or other rating systems).
    """

    def __init__(self, film_id, title, actors, release_year, genre, rating, description, image_path):
        """
        Initializes a Film object.

        Args:
            film_id (str or ObjectId, optional): The unique ID of the film from MongoDB. Defaults to None.
            title (str): The title of the film.
            actors (list): A list of actor surnames.
            release_year (int): The year the film was released.
            genre (str): The genre of the film.
            rating (float): The film's rating (e.g., IMDb rating).
            description (str): The film's description.
            image_path (str): The main image of the film.
        """
        self.film_id = str(film_id) if film_id else None
        self.title = title  # Title of the film
        self.actors = actors  # List or string of actor IDs
        self.release_year = release_year  # Year of release
        self.genre = genre  # Genre of the film
        self.rating = rating  # Film's rating
        self.description = description
        self.image_path = image_path

    def to_dict(self):
        """
        Converts the Film object into a dictionary format.

        Returns:
            dict: A dictionary with the film's details, suitable for JSON serialization.
        """
        return {
            "_id": self.film_id,
            "title": self.title,
            "actors": self.actors,
            "release_year": self.release_year,
            "genre": self.genre,
            "rating": self.rating,
            "description": self.description,
            "image_path": self.image_path
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Film instance from a dictionary.

        Args:
            data (dict): A dictionary containing film details. Expected keys are:
                - "title" (str): Title of the film.
                - "actors" (list or str): List or string of actor IDs.
                - "release_year" (int): Year the film was released.
                - "genre" (str): Genre of the film.
                - "rating" (float): Rating of the film.
                - description (str): The film's description.
                - image_path (str): The main image of the film.

        Returns:
            Film: An instance of the Film class initialized with the provided data.
        """
        return Film(
            film_id=data.get("_id"),
            title=data.get("title"),
            actors=data.get("actors"),
            release_year=data.get("release_year"),
            genre=data.get("genre"),
            rating=data.get("rating"),
            description=data.get("description"),
            image_path=data.get("image_path")
        )
