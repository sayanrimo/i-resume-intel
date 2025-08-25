# test_api.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load the .env file to get the token
load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

print("--- Hugging Face API Connection Test ---")

if not token:
    print("Error: HUGGINGFACEHUB_API_TOKEN not found in your .env file.")
else:
    print(f"Found token starting with: {token[:5]}...")
    try:
        # Initialize the client with your token
        client = InferenceClient(token=token)

        # Use the standard, reliable model
        model_id = "google/flan-t5-base"
        print(f"Attempting to call model: {model_id}")

        # Make the direct API call
        response = client.text_generation(
            prompt="What is the capital of India?",
            model=model_id,
            max_new_tokens=20
        )

        print("\n--- ✅ SUCCESS! ---")
        print("The API call was successful.")
        print(f"Response from model: {response}")

    except Exception as e:
        print("\n--- ❌ FAILED! ---")
        print("The API call failed. This confirms a network or environment issue.")
        print("The most likely cause is a Firewall, Antivirus, or VPN.")
        print(f"\nError details: {e}")

print("--- Test Complete ---")