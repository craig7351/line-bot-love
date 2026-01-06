import os
from google import genai
from google.genai import types

def process_message(text, user_id=None):
    """
    Takes an input message and returns a warmer, more polite version using the Google GenAI SDK.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "System Error: Gemini API Key missing."

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a warm, polite, and emotionally intelligent assistant. 
        Your task is to rewrite the following message to be gentler, more considerate, and "warmer".
        Maintain the original meaning but change the tone to be very caring.
        If the message is already warm, just return it or slightly enhance it.
        
        Original Message: "{text}"
        
        Rewritten Message:
        """
        
        # Using the generate_content method from the new SDK
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
            )
        )
        
        if response.text:
            return response.text.strip()
        
        return "Sorry, I couldn't translate that gently."

    except Exception as e:
        print(f"Error calling Google GenAI SDK: {e}")
        return "Sorry, I am having trouble being warm right now. (SDK Error)"

if __name__ == "__main__":
    # Test cases
    print(process_message("不"))
    print(process_message("幾點了"))
