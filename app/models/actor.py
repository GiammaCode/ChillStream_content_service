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


    def __init__(self, name: str, surname: str, date_of_birth: str, films=None, actor_id=None):
        """
    Initializes an Actor object.

    Args:
        name (str): First name of the actor.
        surname (str): Last name of the actor (must be unique).
        date_of_birth (str): Date of birth of the actor in 'YYYY-MM-DD' format.
        films (list, optional): List of film ObjectIds (default is empty list).
        actor_id (str, optional): MongoDB ObjectId (default is None).
    """
        self.actor_id = str(actor_id) if actor_id else None
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.films = films if films else []

    def to_dict(self):
        """
    Converts the Actor object into a dictionary format.
    """

        return {
            "_id": self.actor_id,  # MongoDB usa _id
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "films": self.films  # Lista di ObjectId in stringa
        }

    @staticmethod
    def from_dict(data):
        """
    Creates an Actor instance from a dictionary.
    """
        return Actor(
            actor_id=data.get("_id"),
            name=data.get("name"),
            surname=data.get("surname"),
            date_of_birth=data.get("date_of_birth"),
            films=data.get("films", [])
        )
