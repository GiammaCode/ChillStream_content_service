from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/<string:film_id>/reviews", methods=["GET"])
def get_reviews(film_id):
    try:
        film_object_id = ObjectId(film_id)
    except Exception as e:
        return jsonify({"error": "Invalid Film ID format"}), 400

    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    reviews = list(mongo.db.reviews.find({"film_id": film_id}))

    for review in reviews:
        review["_id"] = str(review["_id"])
        review["film_id"] = str(review["film_id"])
        review["profile_id"] = str(review["profile_id"])

    return jsonify({"film_id": film_id, "reviews": reviews}), 200

@reviews_bp.route("/<string:film_id>/reviews", methods=["POST"])
def add_review(film_id):
    """
    Add a new review for a specific film.

    Request Body:
        JSON: { "profile_id": "65d3e8a67f3b5b8c21e4d9f6", "text": "Great movie!" }

    Returns:
        Response: Success message or error message.
    """
    data = request.json

    # Controllo se `film_id` è valido
    try:
        film_object_id = ObjectId(film_id)
    except Exception as e:
        return jsonify({"error": "Invalid Film ID format"}), 400

    # Controllo se il film esiste
    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    # Controllo se il profilo utente esiste
    profile_id = data.get("profile_id")
    #profile = mongo.db.profiles.find_one({"_id": ObjectId(profile_id)})
    #if not profile:
        #return jsonify({"error": "Profile not found"}), 404

    # Creazione della recensione
    review_data = {
        "film_id": film_id,
        "profile_id": profile_id,
        "text": data.get("text", "")  # Assicura che "text" sia presente
    }

    result = mongo.db.reviews.insert_one(review_data)
    review_id = str(result.inserted_id)

    # Aggiorna il film aggiungendo il nuovo review_id alla lista
    mongo.db.films.update_one(
        {"_id": film_object_id},
        {"$push": {"reviews": review_id}}
    )

    return jsonify({"message": "Review added", "review_id": review_id}), 201

@reviews_bp.route("/<string:film_id>/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(film_id, review_id):
    """
    Delete a specific review from a film.

    Args:
        film_id (str): The unique ID of the film.
        review_id (str): The unique ID of the review.

    Returns:
        Response: Success or error message.
    """
    try:
        # Controllo se gli ID sono validi
        film_object_id = ObjectId(film_id)
        review_object_id = ObjectId(review_id)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

    # Controllo se il film esiste
    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    review = mongo.db.reviews.find_one({"_id": review_object_id})
    if not review:
        return jsonify({"error": "Review not found"}), 404

    # Elimina la recensione dal database
    result = mongo.db.reviews.delete_one({"_id": review_object_id})

    # Rimuovi l'ID della recensione dalla lista reviews del film
    mongo.db.films.update_one(
        {"_id": film_object_id},
        {"$pull": {"reviews": review_id}}
    )

    return jsonify({"message": "Review deleted"}), 204
