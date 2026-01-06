from bot_logic import process_message
import os
from dotenv import load_dotenv

load_dotenv()

def test_warm_translator():
    print("Testing Line Bot - Warm Translator Logic...")
    
    # Check API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is missing in .env file.")
        print("Please create a .env file based on .env.example and add your API key.")
        return

    test_cases = [
        "要回來了沒! 幾點了",
        "不",
        "滾",
        "你煩不煩"
    ]

    for msg in test_cases:
        print("-" * 30)
        print(f"Original: {msg}")
        warm_msg = process_message(msg)
        print(f"Warm:     {warm_msg}")

if __name__ == "__main__":
    test_warm_translator()
