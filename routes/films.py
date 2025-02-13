"""
API Blueprint for Film Management

This module defines API routes for managing film-related operations, including
retrieving, adding, updating, and deleting films.

Blueprint:
    - `films_bp`: A Flask Blueprint for film-related routes.

Routes:
    1. `GET /`: Retrieve a list of all films.
    2. `POST /`: Add a new film to the database.
    3. `GET /<int:filmId>`: Retrieve details of a specific film by its ID.
    4. `PUT /<int:filmId>`: Update the details of a specific film by its ID.
    5. `DELETE /<int:filmId>`: Delete a specific film by its ID.

Dependencies:
    - Flask: For routing and handling HTTP requests.
    - pymongo: For database operations with MongoDB.
    - utils.validation.validate_film: For validating film input data.
"""

from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_film

# Define the Blueprint
films_bp = Blueprint("films", __name__)

@films_bp.route("/", methods=["GET"])
def get_films():
    """
    Retrieve all films from the database.

    Returns:
        Response: A JSON response with a list of films and status code 200.
    """
    films = list(mongo.db.films.find())
    for film in films:
        film["_id"] = str(film["_id"])  # Convert ObjectId to string for serialization
    return jsonify(films), 200

@films_bp.route("/", methods=["POST"])
def add_films():
    """
    Add new film(s) to the database.

    Request Body:
        JSON: A single film or a list of films (validated using `validate_film`).

    Returns:
        Response:
            - 201: Success message if the film(s) are added.
            - 400: Error message if validation fails.
    """
    data = request.json

    # Check if the input is a list or a single object
    if isinstance(data, list):
        errors = []

        for film in data:
            valid, error = validate_film(film)
            if not valid:
                errors.append({"film": film, "error": error})
                continue

            # Insert the film into the database
            mongo.db.films.insert_one(film)

            # Update each actor's films list
            update_actors_with_film(film)

        if errors:
            return jsonify({
                "message": "Some films were not added",
                "errors": errors
            }), 400

        return jsonify({"message": "Films added and actors updated successfully"}), 201

    # Handle a single film
    valid, error = validate_film(data)
    if not valid:
        return jsonify(error), 400

    # Insert the film into the database
    mongo.db.films.insert_one(data)

    # Update each actor's films list
    update_actors_with_film(data)

    return jsonify({"message": "Film added and actors updated successfully"}), 201

def update_actors_with_film(film):
    """
    Update the films list for each actor involved in the film.

    Args:
        film (dict): The film data, including the "actors" field.
    """
    actor_ids = film.get("actors", [])

    # Handle actors provided as a comma-separated string
    if isinstance(actor_ids, str):
        actor_ids = [int(actor_id.strip()) for actor_id in actor_ids.split(",")]

    for actor_id in actor_ids:
        actor = mongo.db.actors.find_one({"actorId": actor_id})
        if actor:
            existing_films = actor.get("films", "").split(", ")
            if str(film["filmId"]) not in existing_films:
                updated_films = ", ".join(filter(None, [str(film["filmId"])] + existing_films))
                mongo.db.actors.update_one(
                    {"actorId": actor_id},
                    {"$set": {"films": updated_films}}
                )

@films_bp.route("/<int:filmId>", methods=["GET"])
def get_film(filmId):
    """
    Retrieve details of a specific film by its filmId.

    Args:
        filmId (int): The unique ID of the film.

    Returns:
        Response:
            - 200: Film details if found.
            - 404: Error message if the film is not found.
    """
    film = mongo.db.films.find_one({"filmId": filmId})
    if film:
        film["_id"] = str(film["_id"])
        return jsonify(film), 200
    return jsonify({"error": "Film not found"}), 404

@films_bp.route("/<int:filmId>", methods=["PUT"])
def update_film(filmId):
    """
    Update details of a specific film by its filmId.

    Args:
        filmId (int): The unique ID of the film.

    Request Body:
        JSON: Updated film details.

    Returns:
        Response:
            - 200: Updated film details if successful.
            - 404: Error message if the film is not found.
    """
    data = request.json
    updated_film = mongo.db.films.find_one_and_update(
        {"filmId": filmId},
        {"$set": data},
        return_document=True
    )
    if updated_film:
        updated_film["_id"] = str(updated_film["_id"])
        return jsonify(updated_film), 200
    return jsonify({"error": "Film not found"}), 404

@films_bp.route("/<int:filmId>", methods=["DELETE"])
def delete_film(filmId):
    """
    Delete a specific film by its filmId.

    Args:
        filmId (int): The unique ID of the film.

    Returns:
        Response:
            - 204: No content if deletion is successful.
            - 404: Error message if the film is not found.
    """
    result = mongo.db.films.delete_one({"filmId": filmId})
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Film ID not found"}), 404

@films_bp.route("/<int:filmId>/actors", methods=["GET"])
def get_actors_by_film(filmId):
    """
    Retrieve a list of actors associated with a specific film.

    Args:
        filmId (int): The unique ID of the film.

    Returns:
        Response:
            - 200: List of associated actors if successful.
            - 400: Error message if the actor ID format is invalid.
            - 404: Error message if the film is not found.
    """
    # Trova il film corrispondente all'ID
    film = mongo.db.films.find_one({"filmId": filmId})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    # Recupera gli ID degli attori dal film
    actor_ids = film.get("actors", [])

    # Se gli ID sono stringhe, separali e rimuovi gli spazi
    if isinstance(actor_ids, str):
        actor_ids = [id_.strip() for id_ in actor_ids.split(",")]

    try:
        # Converti gli ID in formato integer
        actor_ids = [int(actor_id) for actor_id in actor_ids if actor_id.isdigit()]
    except ValueError:
        return jsonify({"error": "Invalid actor ID format"}), 400

    if not actor_ids:
        return jsonify({"actors": []}), 200

    # Trova gli attori corrispondenti
    actors = list(mongo.db.actors.find({"actorId": {"$in": actor_ids}}))
    for actor in actors:
        actor["_id"] = str(actor["_id"])  # Converti ObjectId in stringa per la serializzazione

    return jsonify({"filmId": filmId, "actors": actors}), 200
