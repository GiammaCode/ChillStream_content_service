class Actor:
    """
    Represents an actor with their personal details and a list of films they have acted in.

    Attributes:
        actorId (int): Unique identifier for the actor.
        name (str): First name of the actor.
        surname (str): Last name of the actor.
        date_of_birth (str): Date of birth of the actor in string format (e.g., 'YYYY-MM-DD').
        films (str): Comma-separated list of film IDs representing movies the actor has participated in.
    """

    def __init__(self, actorId: int, name: str, surname: str, date_of_birth: str, films: str):
        """
        Initializes an Actor object.

        Args:
            actorId (int): The unique identifier for the actor.
            name (str): The first name of the actor.
            surname (str): The last name of the actor.
            date_of_birth (str): The date of birth of the actor in 'YYYY-MM-DD' format.
            films (str): A comma-separated string of film IDs.
        """
        self.actorId = actorId  # Unique ID of the actor
        self.name = name  # First name of the actor
        self.surname = surname  # Last name of the actor
        self.date_of_birth = date_of_birth  # Date of birth in 'YYYY-MM-DD' format
        self.films = films  # Comma-separated list of film IDs

    def to_dict(self):
        """
        Converts the Actor object into a dictionary format.

        Returns:
            dict: A dictionary with the actor's details, suitable for JSON serialization.
        """
        return {
            "actorId": self.actorId,
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "films": self.films,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates an Actor instance from a dictionary.

        Args:
            data (dict): A dictionary containing actor details. Expected keys are:
                - "id" (int): Unique identifier for the actor.
                - "name" (str): First name of the actor.
                - "surname" (str): Last name of the actor.
                - "dateOfBirth" (str): Date of birth of the actor in 'YYYY-MM-DD' format.
                - "films" (str): Comma-separated string of film IDs.

        Returns:
            Actor: An instance of the Actor class initialized with the provided data.
        """
        return Actor(
            actorId=data.get("id"),
            name=data.get("name"),
            surname=data.get("surname"),
            date_of_birth=data.get("dateOfBirth"),
            films=data.get("films"),
        )

