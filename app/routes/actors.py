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
    3. `GET /<int:actor_id>`: Retrieve details of a specific actor by their ID.
    4. `PUT /<int:actor_id>`: Update the details of a specific actor by their ID.
    5. `DELETE /<int:actor_id>`: Remove a specific actor by their ID.
    6. `GET /<int:actor_id>/films`: Retrieve a list of films associated with a specific actor.

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
def add_actors():
    """
    Add multiple actors to the database.
    """
    data = request.json  # Riceve una lista di attori

    if not isinstance(data, list):  # Controllo per garantire che sia una lista
        return jsonify({"error": "Input data must be a list of actors"}), 400

    actors_to_insert = []  # Lista per gli attori validi

    for actor in data:
        # Controlla se tutti i campi necessari sono presenti
        if "name" not in actor or "surname" not in actor or "date_of_birth" not in actor:
            return jsonify({"error": "Missing required fields in one or more records"}), 400

        # Controlla se l'attore esiste già nel database
        existing_actor = db.actors.find_one({"surname": actor["surname"]})
        if existing_actor:
            continue  # Salta l'inserimento se l'attore esiste già

        # Crea l'oggetto per il database
        actors_to_insert.append({
            "name": actor["name"],
            "surname": actor["surname"],
            "date_of_birth": actor["date_of_birth"],
            "films": []  # Lista vuota di film
        })

    # Se ci sono attori da inserire, esegui l'inserimento batch
    if actors_to_insert:
        result = db.actors.insert_many(actors_to_insert)
        return jsonify({
            "message": f"{len(result.inserted_ids)} actors added",
            "actor_ids": [str(actor_id) for actor_id in result.inserted_ids]
        }), 201
    else:
        return jsonify({"message": "No new actors were added"}), 200


@actors_bp.route("/<string:actor_id>", methods=["GET"])
def get_actor_by_id(actor_id):
    """
    Retrieve details of a specific actor by their actor_id.

    Args:
        actor_id (string): The unique ID of the actor.

    Returns:
        Response:
            - 200: Actor details if found.
            - 404: Error message if the actor is not found.
    """
    try:
        actor = mongo.db.actors.find_one({"_id": ObjectId(actor_id)})
        if actor:
            actor["_id"] = str(actor["_id"])
            return jsonify(actor), 200
        return jsonify({"error": "Actor not found"}), 404
    except:
        return jsonify({"error": "Invalid actor ID"}), 400


@actors_bp.route("/<string:actor_id>", methods=["PUT"])
def update_actor(actor_id):
    """
    Update details of a specific actor by their actor_id.

    Args:
        actor_id (string): The unique ID of the actor.

    Request Body:
        JSON: Updated actor details.

    Returns:
        Response:
            - 200: Updated actor details if successful.
            - 404: Error message if the actor is not found.
    """
    data = request.json
    updated_actor = mongo.db.actors.find_one_and_update(
        {"_id": ObjectId(actor_id)},
        {"$set": data},
        return_document=True
    )
    if updated_actor:
        updated_actor["_id"] = str(updated_actor["_id"])
        return jsonify(updated_actor), 200
    return jsonify({"error": "Actor not found"}), 404


@actors_bp.route("/<string:actor_id>", methods=["DELETE"])
def delete_actor(actor_id):
    """
    Delete a specific actor by their actor_id.

    Args:
        actor_id (string): The unique ID of the actor.

    Returns:
        Response:
            - 204: No content if deletion is successful.
            - 404: Error message if the actor is not found.
    """
    result = mongo.db.actors.delete_one({"_id": ObjectId(actor_id)})
    if result.deleted_count > 0:
        return "", 204
    return jsonify({"error": "Actor not found"}), 404


@actors_bp.route("/<string:actor_id>/films", methods=["GET"])
def get_films_by_actor(actor_id):
    """
    Retrieve a list of films associated with a specific actor.

    Args:
        actor_id (string): The unique ID of the actor.

    Returns:
        Response:
            - 200: List of associated films if successful.
            - 400: Error message if the film ID format is invalid.
            - 404: Error message if the actor is not found.
    """
    try:
        # Converti actor_id in ObjectId
        actor_object_id = ObjectId(actor_id)
    except:
        return jsonify({"error": "Invalid Actor ID format"}), 400

    # Cerca l'attore nel database
    actor = mongo.db.actors.find_one({"_id": actor_object_id})
    if not actor:
        return jsonify({"error": "Actor not found"}), 404

    # Estrai la lista dei film associati all'attore
    film_ids = actor.get("films", [])

    # Assicurati che `film_ids` sia una lista di ObjectId validi
    if not isinstance(film_ids, list):
        return jsonify({"error": "Invalid film list format"}), 400

    try:
        # Converti gli ID in ObjectId e cerca i film nel database
        film_object_ids = [ObjectId(film_id) for film_id in film_ids]
        films = list(mongo.db.films.find({"_id": {"$in": film_object_ids}}))

        # Converti gli ObjectId in stringa per la serializzazione JSON
        for film in films:
            film["_id"] = str(film["_id"])

        return jsonify({"_id": actor_id, "films": films}), 200

    except Exception as e:
        return jsonify({"error": "Error retrieving films", "details": str(e)}), 500
