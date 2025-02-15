from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo
from models.review import Review

# Creazione del Blueprint per le recensioni
reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/films/<string:film_id>/reviews", methods=["GET"])
def get_reviews(film_id):
    """
    Retrieve all reviews for a specific film.

    Args:
        film_id (str): The unique ID of the film.

    Returns:
        Response: A JSON list of reviews or an error message.
    """
    try:
        reviews = list(mongo.db.reviews.find({"film_id": ObjectId(film_id)}))
        for review in reviews:
            review["_id"] = str(review["_id"])
            review["film_id"] = str(review["film_id"])
            review["profile_id"] = str(review["profile_id"])
        return jsonify(reviews), 200
    except:
        return jsonify({"error": "Invalid Film ID"}), 400

@reviews_bp.route("/films/<string:film_id>/reviews", methods=["POST"])
def add_review(film_id):
    """
    Add a new review for a specific film.

    Request Body:
        JSON: { "profile_id": "65d3e8a67f3b5b8c21e4d9f6", "text": "Great movie!" }

    Returns:
        Response: Success message or error message.
    """
    data = request.json

    # Controlla che il film esista
    film = mongo.db.films.find_one({"_id": ObjectId(film_id)})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    # Controlla che il profilo esista
    profile = mongo.db.profiles.find_one({"_id": ObjectId(data["profile_id"])})
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    review_data = {
        "film_id": ObjectId(film_id),
        "profile_id": ObjectId(data["profile_id"]),
        "text": data["text"]
    }

    result = mongo.db.reviews.insert_one(review_data)

    return jsonify({"message": "Review added", "review_id": str(result.inserted_id)}), 201

@reviews_bp.route("/films/<string:film_id>/reviews/<string:review_id>", methods=["DELETE"])
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
        result = mongo.db.reviews.delete_one({"_id": ObjectId(review_id), "film_id": ObjectId(film_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Review deleted"}), 204
        return jsonify({"error": "Review not found"}), 404
    except:
        return jsonify({"error": "Invalid Review ID"}), 400
