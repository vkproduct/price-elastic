from flask import jsonify

def handle_404_error(e):
    return jsonify({"error": "Not found", "message": "The requested resource does not exist"}), 404

def handle_500_error(e):
    return jsonify({"error": "Server error", "message": "An unexpected server error occurred"}), 500