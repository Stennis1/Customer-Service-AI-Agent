import os 
from openai import OpenAI
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()

# Test OpenAI connection 
try: 
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hello, world!"}
        ],
        max_tokens=50
    )
    
    print("✅ OpenAI API connection successful")
    print(f"Response: {response.choices[0].message.content}")

except Exception as e:
    print(f"❌ OpenAI API error: {e}")

print("🎉 Setup verification complete!")