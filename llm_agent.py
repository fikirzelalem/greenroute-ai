# llm_agent.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Base NVIDIA endpoint
NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY = os.getenv("NGC_API_KEY")

# Primary (Nemotron) and fallback (Stockmark) models
PRIMARY_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
FALLBACK_MODEL = "stockmark/stockmark-2-100b-instruct"


def call_nemotron(routes):
    """
    Calls the NVIDIA Nemotron model (with Stockmark fallback) 
    to reason about the greener route between two destinations.
    """
    if not API_KEY:
        return "⚠️ No NVIDIA API key found. Please check your .env file."

    # Build the reasoning prompt
    prompt = "You are a sustainability routing assistant. Compare these routes and recommend the greener one:\n"
    for r in routes:
        prompt += f"- {r['route']}: distance {r['distance']} km, time {r['time']} min, CO₂ {r['co2']:.2f} kg, AQI {r['aqi']}\n"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Try Nemotron first
    payload = {
        "model": PRIMARY_MODEL,
        "messages": [
            {"role": "system", "content": "You are an environmental route advisor AI."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 300,
    }

    try:
        response = requests.post(NIM_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        else:
            # 🔁 Fallback to Stockmark if Nemotron returns 404 or error
            print(f"⚠️ Nemotron error {response.status_code}: {response.text}")
            return call_fallback_model(prompt, headers)

    except Exception as e:
        print(f"⚠️ Nemotron connection error: {e}")
        return call_fallback_model(prompt, headers)


def call_fallback_model(prompt, headers):
    """
    Uses Stockmark-2-100B-Instruct if Nemotron fails.
    """
    fallback_payload = {
        "model": FALLBACK_MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI route analysis assistant."},
            {"role": "user", "content": prompt + "\nProvide a short sustainability-based recommendation."},
        ],
        "temperature": 0.7,
        "max_tokens": 250,
    }

    try:
        response = requests.post(NIM_URL, headers=headers, json=fallback_payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return (
                "🤖 (Fallback Model Used)\n" + data["choices"][0]["message"]["content"].strip()
            )
        else:
            return f"⚠️ Fallback model also failed ({response.status_code})."

    except Exception as e:
        return f"⚠️ Error contacting fallback model: {e}"
