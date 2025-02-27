from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/<string:film_id>/reviews", methods=["GET"])
def get_reviews(film_id):
    """ Get all reviews for a specific film. """
    try:
        film_object_id = ObjectId(film_id)
    except Exception:
        return jsonify({"error": "Invalid Film ID format"}), 400

    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    reviews = list(mongo.db.reviews.find({"film_id": film_id}))

    formatted_reviews = []
    for review in reviews:
        formatted_reviews.append({
            "_id": str(review["_id"]),
            "film_id": str(review["film_id"]),
            "nickname": review.get("nickname", ""),
            "profile_id": str(review["profile_id"]),
            "text": review["text"]
        })

    return jsonify(formatted_reviews), 200


@reviews_bp.route("/<string:film_id>/reviews", methods=["POST"])
def add_review(film_id):
    """ Add a new review for a specific film. """
    data = request.json

    try:
        film_object_id = ObjectId(film_id)
    except Exception:
        return jsonify({"error": "Invalid Film ID format"}), 400

    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    profile_id = data.get("profile_id")
    nickname = data.get("nickname")
    text = data.get("text", "")

    if not profile_id or not nickname or not text:
        return jsonify({"error": "Missing required fields"}), 400

    review_data = {
        "film_id": film_id,
        "profile_id": profile_id,
        "nickname": nickname,
        "text": text
    }

    result = mongo.db.reviews.insert_one(review_data)
    review_id = str(result.inserted_id)

    mongo.db.films.update_one(
        {"_id": film_object_id},
        {"$push": {"reviews": review_id}}
    )

    return jsonify({"message": "Review added", "review_id": review_id}), 201


@reviews_bp.route("/<string:film_id>/reviews/<string:review_id>", methods=["GET"])
def get_single_review(film_id, review_id):
    """ Get a single review by review_id. """
    try:
        review_object_id = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid Review ID format"}), 400

    review = mongo.db.reviews.find_one({"_id": review_object_id})
    if not review:
        return jsonify({"error": "Review not found"}), 404

    formatted_review = {
        "_id": str(review["_id"]),
        "film_id": str(review["film_id"]),
        "nickname": review.get("nickname", ""),
        "profile_id": str(review["profile_id"]),
        "text": review["text"]
    }

    return jsonify(formatted_review), 200


@reviews_bp.route("/<string:film_id>/reviews/<string:review_id>", methods=["PUT"])
def update_review(film_id, review_id):
    """ Update a review's text or nickname. """
    data = request.json

    try:
        review_object_id = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid Review ID format"}), 400

    update_fields = {key: data[key] for key in ["text", "nickname"] if key in data}

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    updated_review = mongo.db.reviews.find_one_and_update(
        {"_id": review_object_id},
        {"$set": update_fields},
        return_document=True
    )

    if not updated_review:
        return jsonify({"error": "Review not found"}), 404

    return jsonify({"message": "Review updated", "review": {
        "_id": str(updated_review["_id"]),
        "film_id": str(updated_review["film_id"]),
        "nickname": updated_review.get("nickname", ""),
        "profile_id": str(updated_review["profile_id"]),
        "text": updated_review["text"]
    }}), 200


@reviews_bp.route("/<string:film_id>/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(film_id, review_id):
    """ Delete a specific review from a film. """
    try:
        film_object_id = ObjectId(film_id)
        review_object_id = ObjectId(review_id)
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

    film = mongo.db.films.find_one({"_id": film_object_id})
    if not film:
        return jsonify({"error": "Film not found"}), 404

    review = mongo.db.reviews.find_one({"_id": review_object_id})
    if not review:
        return jsonify({"error": "Review not found"}), 404

    mongo.db.reviews.delete_one({"_id": review_object_id})

    mongo.db.films.update_one(
        {"_id": film_object_id},
        {"$pull": {"reviews": review_id}}
    )

    return jsonify({"message": "Review deleted"}), 204
