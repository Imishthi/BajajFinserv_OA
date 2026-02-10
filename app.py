from flask import Flask, request, jsonify

app = Flask(__name__)

OFFICIAL_EMAIL = "mishthi3877.bei23@chitkara.edu.in"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route("/bfhl", methods=["POST"])
def bfhl():
    data = request.get_json(force=True)


    if not data or "data" not in data:
        return jsonify({
            "is_success": False,
            "error": "Invalid request"
        }), 400

    arr = data["data"]

    numbers = []
    alphabets = []

    for x in arr:
        if x.isdigit():
            numbers.append(x)
        elif x.isalpha():
            alphabets.append(x)

    highest_alphabet = max(alphabets) if alphabets else None

    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_alphabet": highest_alphabet
    }), 200


if __name__ == "__main__":
    app.run()
