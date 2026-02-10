from flask import Flask, request, jsonify
from dotenv import load_dotenv
import math
import requests
import os

load_dotenv()
app = Flask(__name__)

OFFICIAL_EMAIL = "mishthi3877.bei23@chitkara.edu.in"   
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  



def fibonacci(n):
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def lcm_of_list(arr):
    lcm = arr[0]
    for i in arr[1:]:
        lcm = lcm * i // math.gcd(lcm, i)
    return lcm

def hcf_of_list(arr):
    hcf = arr[0]
    for i in arr[1:]:
        hcf = math.gcd(hcf, i)
    return hcf

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    response = requests.post(url, json=payload)
    result = response.json()
    answer = result["candidates"][0]["content"]["parts"][0]["text"]
    return answer.strip().split()[0]  



@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.get_json()

        if not data or len(data.keys()) != 1:
            return jsonify({
                "is_success": False,
                "error": "Invalid input"
            }), 400

        key = list(data.keys())[0]
        value = data[key]

        if key == "fibonacci":
            if not isinstance(value, int) or value < 0:
                raise ValueError
            result = fibonacci(value)

        elif key == "prime":
            if not isinstance(value, list):
                raise ValueError
            result = [x for x in value if is_prime(x)]

        elif key == "lcm":
            if not isinstance(value, list) or len(value) == 0:
                raise ValueError
            result = lcm_of_list(value)

        elif key == "hcf":
            if not isinstance(value, list) or len(value) == 0:
                raise ValueError
            result = hcf_of_list(value)

        elif key == "AI":
            if not isinstance(value, str):
                raise ValueError
            result = ask_gemini(value)

        else:
            raise ValueError

        return jsonify({
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": result
        }), 200

    except Exception:
        return jsonify({
            "is_success": False,
            "error": "Invalid request"
        }), 400


if __name__ == "__main__":
    app.run()
