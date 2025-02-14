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
from bson import ObjectId

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
    """
    data = request.json

    # Controlla se l'attore esiste già con lo stesso cognome
    existing_actor = mongo.db.actors.find_one({"surname": data["surname"]})
    if existing_actor:
        return jsonify({"error": "Actor with this surname already exists"}), 400

    actor_data = {
        "name": data["name"],
        "surname": data["surname"],
        "date_of_birth": data["date_of_birth"],
        "films": []  # Lista vuota di film
    }

    result = mongo.db.actors.insert_one(actor_data)

    return jsonify({"message": "Actor added", "actor_id": str(result.inserted_id)}), 201

@actors_bp.route("/<int:actorId>", methods=["GET"])
def get_actor_by_id(actor_id):
    """
    Retrieve details of a specific actor by their actorId.

    Args:
        actorId (int): The unique ID of the actor.

    Returns:
        Response:
            - 200: Actor details if found.
            - 404: Error message if the actor is not found.
    """
    actor = mongo.db.actors.find_one({"actorId": actor_id})
    if actor:
        actor["_id"] = str(actor["_id"])
        return jsonify(actor), 200
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>", methods=["PUT"])
def update_actor(actor_id):
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
        {"actorId": actor_id},
        {"$set": data},
        return_document=True
    )
    if updated_actor:
        updated_actor["_id"] = str(updated_actor["_id"])
        return jsonify(updated_actor), 200
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>", methods=["DELETE"])
def delete_actor(actor_id):
    """
    Delete a specific actor by their actorId.

    Args:
        actorId (int): The unique ID of the actor.

    Returns:
        Response:
            - 204: No content if deletion is successful.
            - 404: Error message if the actor is not found.
    """
    result = mongo.db.actors.delete_one({"actorId": actor_id})
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Actor not found"}), 404

@actors_bp.route("/<int:actorId>/films", methods=["GET"])
def get_films_by_actor(actor_id):
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
    try:
        actor = mongo.db.actors.find_one({"_id": ObjectId(actor_id)})
        if actor:
            actor["_id"] = str(actor["_id"])
            return jsonify(actor), 200
        return jsonify({"error": "Actor not found"}), 404
    except:
        return jsonify({"error": "Invalid Actor ID"}), 400
