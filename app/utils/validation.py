"""
Validation Utilities for Actor and Film Data

This module contains functions to validate incoming data for actors and films
to ensure they meet the required structure and data types.

Functions:
    1. `validate_film(data)`: Validates the structure and types of a film's data.
    2. `validate_actor(data)`: Validates the structure and types of an actor's data.
"""

def validate_film(data):
    """
    Validate the structure and data types of a film's data.

    Args:
        data (dict): The data to validate.

    Required Fields:
        - `filmId` (int): Unique identifier for the film.
        - `title` (str): Title of the film.
        - `actors` (str): Comma-separated list or a string representing actor IDs.
        - `release_year` (int): Year the film was released.
        - `genre` (str): Genre of the film.
        - `rating` (int or float): Rating of the film.

    Returns:
        tuple: A boolean indicating validity and a message (None if valid).
            - (True, None): If validation succeeds.
            - (False, dict): If validation fails, with an error message.
    """
    required_fields = {
        "filmId": int,
        "title": str,
        "actors": str,  # Can be a comma-separated string or list
        "release_year": int,
        "genre": str,
        "rating": (int, float),  # Can be either an int or float
    }
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, {"message": f"Missing fields: {', '.join(missing_fields)}"}

    # Validate field types
    for field, field_type in required_fields.items():
        if not isinstance(data[field], field_type):
            return False, {"message": f"Field '{field}' must be of type {field_type.__name__}"}

    return True, None

def validate_actor(data):
    """
    Validate the structure and data types of an actor's data.

    Args:
        data (dict): The data to validate.

    Required Fields:
        - `actorId` (int): Unique identifier for the actor.
        - `name` (str): First name of the actor.
        - `surname` (str): Last name of the actor.
        - `date_of_birth` (str): Birth date in the format "YYYY-MM-DD".
        - `films` (str): Comma-separated string representing film IDs.

    Returns:
        tuple: A boolean indicating validity and a message (None if valid).
            - (True, None): If validation succeeds.
            - (False, dict): If validation fails, with an error message.
    """
    required_fields = {
        "actorId": int,
        "name": str,
        "surname": str,
        "date_of_birth": str,  # Format: "YYYY-MM-DD"
        "films": str,  # Comma-separated string
    }
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, {"message": f"Missing fields: {', '.join(missing_fields)}"}

    # Validate field types
    for field, field_type in required_fields.items():
        if not isinstance(data[field], field_type):
            return False, {"message": f"Field '{field}' must be of type {field_type.__name__}"}

    return True, None
