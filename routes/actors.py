"""
API Blueprint for Actor Management

This module defines API routes for managing actor-related operations, including
retrieving, adding, updating, deleting actors, and fetching associated films.
Y-MM-DD' format.
            films (str): A comma-separated string of film IDs.

Blueprint:
    - `actors_bp`: A Flask Blueprint for actor-related routes.

Routes:
    1. `GET /`: Retrieve a list of all actors.
    2. `POST /`: Add a new actor to the database.
    3. `GET /<int:actorId>`: Retrieve details of a specific actor by their ID.
    4. `PUT /<int:actorId>`: Update the details of a specific actor by their ID.
    5. `DELETE /<int:actorId>`: Remove a specific actor by their ID.
    6. `GET /<int:actorId>/films`: Retrieve a list of films associated with a specific actor.

Dependencies:
    - Flask: For routing and handling HTTP requests.
    - pymongo: For database operations with MongoDB.
    - utils.validation.validate_actor: For validating actor input data.
"""

from flask import Blueprint, request, jsonify
from services.db import mongo
from utils.validation import validate_actor

# Define the Blueprint
actors_bp = Blueprint("actors", __name__)

@actors_bp.route("/", methods=["GET"])
def get_actors():
    """
    Retrieve all actors from the database.

    Returns:
        Response: A JSON response with a list of actors and status code 200.
    """
    actors = list(mongo.db.actors.find())
    for actor in actors:
        actor["_id"] = str(actor["_id"])  # Convert ObjectId to string for serialization
    return jsonify(actors), 200

@actors_bp.route("/", methods=["POST"])
def add_actor():
    """
    Add a new actor to the database.

    Request Body:
        JSON: Actor details (validated using `validate_actor`).

    Returns:
        Response:
            - 201: Success message if the actor is added.
            - 400: Error message if validation fails.
    """
    data = request.json

    # Controlla se il payload è un array
    if isinstance(data, list):
        errors = []
        for actor in data:
            valid, error = validate_actor(actor)
            if not valid:
                errors.append(error)
                continue
            mongo.db.actors.insert_one(actor)

        if errors:
            return jsonify({"message": "Some actors were not added", "errors": errors}), 400

        return jsonify({"message": "Actors added successfully"}), 201

    # Gestione di un singolo oggetto
    valid, error = validate_actor(data)
    if not valid:
        return jsonify(error), 400

    mongo.db.actors.insert_one(data)
    return jsonify({"message": "Actor added successfully"}), 201

@actors_bp.route("/<int:actorId>", methods=["GET"])
def get_actor_by_id(actorId):
    """
    Retrieve details of a specific actor by their actorId.

    Args:
        actorId (int): The unique ID of the actor.

    Returns:
        Response:
            - 200: Actor details if found.
            - 404: Error message if the actor is not found.
    """
    actor = mongo.db.actors.find_one({"actorId": actorId})
    if actor:
        actor["_id"] = str(actor["_id"])
        return jsonify(actor), 200
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>", methods=["PUT"])
def update_actor(actorId):
    """
    Update details of a specific actor by their actorId.

    Args:
        actorId (int): The unique ID of the actor.

    Request Body:
        JSON: Updated actor details.

    Returns:
        Response:
            - 200: Updated actor details if successful.
            - 404: Error message if the actor is not found.
    """
    data = request.json
    updated_actor = mongo.db.actors.find_one_and_update(
        {"actorId": actorId},
        {"$set": data},
        return_document=True
    )
    if updated_actor:
        updated_actor["_id"] = str(updated_actor["_id"])
        return jsonify(updated_actor), 200
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>", methods=["DELETE"])
def delete_actor(actorId):
    """
    Delete a specific actor by their actorId.

    Args:
        actorId (int): The unique ID of the actor.

    Returns:
        Response:
            - 204: No content if deletion is successful.
            - 404: Error message if the actor is not found.
    """
    result = mongo.db.actors.delete_one({"actorId": actorId})
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>/films", methods=["GET"])
def get_films_by_actor(actorId):
    """
    Retrieve a list of films associated with a specific actor.

    Args:
        actorId (int): The unique ID of the actor.

    Returns:
        Response:
            - 200: List of associated films if successful.
            - 400: Error message if the film ID format is invalid.
            - 404: Error message if the actor is not found.
    """
    actor = mongo.db.actors.find_one({"actorId": actorId})
    if actor:
        film_ids = actor.get("films", "").split(", ")
        try:
            film_ids = [int(film_id) for film_id in film_ids]
        except ValueError:
            return jsonify({"error": "Invalid film ID format"}), 400
        films = list(mongo.db.films.find({"filmId": {"$in": film_ids}}))
        for film in films:
            film["_id"] = str(film["_id"])
        return jsonify({"actorId": actorId, "films": films}), 200
    return jsonify({"error": "Actor not found"}), 404
