class Film:
    """
    Represents a film with its details, including title, cast, release year, genre, and rating.

    Attributes:
        filmId (int): Unique identifier for the film.
        title (str): Title of the film.
        actors (list or str): List of actor IDs or a string containing comma-separated actor IDs.
        release_year (int): Year the film was released.
        genre (str): Genre of the film (e.g., 'Drama', 'Action').
        rating (float): Rating of the film (e.g., IMDb or other rating systems).
    """

    def __init__(self, filmId, title, actors, release_year, genre, rating, description, image_path):
        """
        Initializes a Film object.

        Args:
            filmId (int): The unique identifier for the film.
            title (str): The title of the film.
            actors (list or str): A list of actor IDs or a string of comma-separated actor IDs.
            release_year (int): The year the film was released.
            genre (str): The genre of the film.
            rating (float): The film's rating (e.g., IMDb rating).
            description (str): The film's description.
            image_path (str): The main image of the film.
        """
        self.filmId = filmId  # Unique ID of the film
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
            "filmId": self.filmId,
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
                - "filmId" (int): Unique identifier for the film.
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
            filmId=data.get("filmId"),
            title=data.get("title"),
            actors=data.get("actors"),
            release_year=data.get("release_year"),
            genre=data.get("genre"),
            rating=data.get("rating"),
            description=data.get("description"),
            image_path=data.get("image_path")
        )
