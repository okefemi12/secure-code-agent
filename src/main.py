import os
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)


HF_API_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/oke39/llama3-8b-secure-code"

def query_model(payload):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/audit", methods=["POST"])
def audit_code():
    data = request.json
    code_snippet = data.get("code", "")
    
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are Jack a Secure Code Agent. Fix the security vulnerability in the provided code.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{code_snippet}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    
    # We mock the response if no token is present (for CI/CD tests)
    if not HF_API_TOKEN:
         return jsonify({"generated_text": "Mock response: Secure code generated."})

    output = query_model({
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "return_full_text": False}
    })
    
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)