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
        
        IMPORTANT:
        1. Access the output using Traditional Chinese (繁體中文).
        2. Do NOT add the prefix in the generated text, I will add it myself.
        3. If the message is NOT a conversational sentence (e.g., just a URL, numbers, a single symbol, code, or gibberish), return EXACTLY the string "NO_RESPONSE".
        
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
            cleaned_text = response.text.strip()
            if "NO_RESPONSE" in cleaned_text:
                return None
            return f"暖心幫回：\n{cleaned_text}"
        
        return "Sorry, I couldn't translate that gently."

    except Exception as e:
        print(f"Error calling Google GenAI SDK: {e}")
        return "Sorry, I am having trouble being warm right now. (SDK Error)"

if __name__ == "__main__":
    # Test cases
    print(process_message("不"))
    print(process_message("幾點了"))
