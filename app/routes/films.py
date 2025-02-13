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

    if isinstance(data, list):
        errors = []
        inserted_ids = []

        for film in data:
            valid, error = validate_film(film)
            if not valid:
                errors.append({"film": film, "error": error})
                continue

            # Insert the film and get the generated _id
            result = mongo.db.films.insert_one(film)
            film["_id"] = str(result.inserted_id)  # Convert ObjectId to string
            inserted_ids.append(film["_id"])

            # Update actors with this film
            update_actors_with_film(film)

        if errors:
            return jsonify({"message": "Some films were not added", "errors": errors}), 400

        return jsonify({"message": "Films added successfully", "inserted_ids": inserted_ids}), 201

    # Handle a single film
    valid, error = validate_film(data)
    if not valid:
        return jsonify(error), 400

    result = mongo.db.films.insert_one(data)
    data["_id"] = str(result.inserted_id)

    update_actors_with_film(data)

    return jsonify({"message": "Film added successfully", "film_id": data["_id"]}), 201

def update_actors_with_film(film):
    """
    Update the films list for each actor involved in the film.
    """
    actor_ids = film.get("actors", [])

    if isinstance(actor_ids, str):
        actor_ids = [actor_id.strip() for actor_id in actor_ids.split(",")]

    for actor_id in actor_ids:
        actor = mongo.db.actors.find_one({"actorId": int(actor_id)})
        if actor:
            existing_films = actor.get("films", "").split(", ")
            if str(film["_id"]) not in existing_films:
                updated_films = ", ".join(filter(None, [str(film["_id"])] + existing_films))
                mongo.db.actors.update_one(
                    {"actorId": int(actor_id)},
                    {"$set": {"films": updated_films}}
                )

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
