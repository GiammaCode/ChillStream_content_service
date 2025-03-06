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
    Add multiple films to the database.
    """
    data = request.json  # Riceve una lista di film

    if not isinstance(data, list):  # Controllo per garantire che sia una lista
        return jsonify({"error": "Input data must be a list of films"}), 400

    films_to_insert = []  # Lista per i film validi
    actor_updates = {}  # Dizionario per tracciare gli aggiornamenti sugli attori

    for film in data:
        # Controllo campi richiesti
        if not all(k in film for k in ["title", "actors", "release_year", "genre", "rating", "description", "image_path"]):
            return jsonify({"error": "Missing required fields in one or more records"}), 400

        # Trova gli attori basandosi sul cognome e ottieni i loro ObjectId
        actor_surnames = film.get("actors", [])
        actor_ids = []

        for surname in actor_surnames:
            actor = mongo.db.actors.find_one({"surname": surname})
            if actor:
                actor_id = str(actor["_id"])
                actor_ids.append(actor_id)

                # Tracciamo quali attori dovranno essere aggiornati
                if actor_id not in actor_updates:
                    actor_updates[actor_id] = []

        # Creiamo il film
        film_data = {
            "title": film["title"],
            "actors": actor_ids,
            "release_year": film["release_year"],
            "genre": film["genre"],
            "rating": film["rating"],
            "description": film["description"],
            "image_path": film["image_path"],
            "reviews": []
        }
        films_to_insert.append(film_data)

    # Inseriamo tutti i film in un'unica operazione se ce ne sono
    if films_to_insert:
        result = mongo.db.films.insert_many(films_to_insert)
        inserted_ids = [str(film_id) for film_id in result.inserted_ids]

        # Aggiorniamo gli attori per collegare i nuovi film
        for film_data, film_id in zip(films_to_insert, inserted_ids):
            for actor_id in film_data["actors"]:
                actor_updates[actor_id].append(film_id)

        # Eseguiamo gli aggiornamenti sugli attori in batch
        for actor_id, film_ids in actor_updates.items():
            mongo.db.actors.update_one(
                {"_id": ObjectId(actor_id)},
                {"$push": {"films": {"$each": film_ids}}}
            )

        return jsonify({
            "message": f"{len(inserted_ids)} films added",
            "film_ids": inserted_ids
        }), 201

    return jsonify({"message": "No films were added"}), 200


@films_bp.route("/<string:film_id>", methods=["GET"])
def get_film_by_id(film_id):
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
