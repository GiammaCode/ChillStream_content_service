from flask import Blueprint, request, jsonify
from bson import ObjectId
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
    """
    data = request.json

    # Trova gli attori basandosi sul cognome e ottieni i loro ObjectId
    actor_surnames = data.get("actors", [])
    actor_ids = []
    for surname in actor_surnames:
        actor = mongo.db.actors.find_one({"surname": surname})
        if actor:
            actor_ids.append(str(actor["_id"]))  # Convertiamo in stringa

    # Creiamo il film
    film_data = {
        "title": data["title"],
        "actors": actor_ids,  # Lista di ObjectId degli attori
        "release_year": data["release_year"],
        "genre": data["genre"],
        "rating": data["rating"],
        "description": data["description"],
        "image_path": data["image_path"]
    }

    result = mongo.db.films.insert_one(film_data)
    film_id = str(result.inserted_id)

    # Aggiorniamo la lista dei film negli attori
    for actor_id in actor_ids:
        mongo.db.actors.update_one(
            {"_id": ObjectId(actor_id)},
            {"$push": {"films": film_id}}
        )

    return jsonify({"message": "Film added", "film_id": film_id}), 201

@films_bp.route("/<string:film_id>", methods=["GET"])
def get_film(film_id):
    """
    Retrieve details of a specific film by its MongoDB _id.
    """
    try:
        film = mongo.db.films.find_one({"_id": ObjectId(film_id)})
        if film:
            film["_id"] = str(film["_id"])
            return jsonify(film), 200
        return jsonify({"error": "Film not found"}), 404
    except:
        return jsonify({"error": "Invalid Film ID"}), 400


@films_bp.route("/<string:film_id>", methods=["PUT"])
def update_film(film_id):
    """
    Update details of a specific film by its MongoDB _id.
    """
    try:
        data = request.json
        updated_film = mongo.db.films.find_one_and_update(
            {"_id": ObjectId(film_id)},
            {"$set": data},
            return_document=True
        )
        if updated_film:
            updated_film["_id"] = str(updated_film["_id"])
            return jsonify(updated_film), 200
        return jsonify({"error": "Film not found"}), 404
    except:
        return jsonify({"error": "Invalid Film ID"}), 400


@films_bp.route("/<string:film_id>", methods=["DELETE"])
def delete_film(film_id):
    """
    Delete a specific film by its MongoDB _id.
    """
    try:
        result = mongo.db.films.delete_one({"_id": ObjectId(film_id)})
        if result.deleted_count > 0:
            return "", 204
        return jsonify({"error": "Film not found"}), 404
    except:
        return jsonify({"error": "Invalid Film ID"}), 400


@films_bp.route("/<string:film_id>/actors", methods=["GET"])
def get_actors_by_film(film_id):
    """
    Retrieve a list of actors associated with a specific film.
    """
    try:
        film = mongo.db.films.find_one({"_id": ObjectId(film_id)})
        if not film:
            return jsonify({"error": "Film not found"}), 404

        actor_ids = film.get("actors", [])

        if isinstance(actor_ids, str):
            actor_ids = [id_.strip() for id_ in actor_ids.split(",")]

        try:
            actor_ids = [int(actor_id) for actor_id in actor_ids if actor_id.isdigit()]
        except ValueError:
            return jsonify({"error": "Invalid actor ID format"}), 400

        if not actor_ids:
            return jsonify({"actors": []}), 200

        actors = list(mongo.db.actors.find({"actorId": {"$in": actor_ids}}))
        for actor in actors:
            actor["_id"] = str(actor["_id"])

        return jsonify({"film_id": film_id, "actors": actors}), 200
    except:
        return jsonify({"error": "Invalid Film ID"}), 400
