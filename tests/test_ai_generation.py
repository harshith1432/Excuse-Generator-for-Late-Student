import os
import sys
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from backend.ai_client import ai_client

def test_excuse_generation():
    print("Testing AI Excuse Generation...")
    situation = "Late to office due to unexpected rain and traffic"
    prompt = f"Generate a highly believable and professional excuse for the following situation: '{situation}'. Provide 3 different variations: one formal, one casual, and one concise. Return ONLY the variations separated by '---'."
    response = ai_client.generate_text(prompt)
    print(f"Response:\n{response}")
    return "Error" not in response and "---" in response

def test_letter_generation():
    print("\nTesting AI Letter Generation...")
    prompt = "Write a professional Leave Application for the following details:\n- Recipient: Principal\n- Subject: Sick Leave\n- Reason/Context: High fever\n- From: Harshith (Class 10)\n- Date: March 15, 2026\nReturn ONLY the letter content."
    response = ai_client.generate_text(prompt)
    print(f"Response:\n{response}")
    return "Error" not in response and len(response) > 100

def test_smart_reply():
    print("\nTesting AI Smart Reply...")
    message = "Can we meet tomorrow at 10 AM to discuss the project?"
    prompt = f"Generate an intelligent and Professional reply to the following message:\n\"{message}\"\nThe reply should be helpful, clear, and maintain the specified tone. Return ONLY the reply text."
    response = ai_client.generate_text(prompt)
    print(f"Response:\n{response}")
    return "Error" not in response and len(response) > 20

if __name__ == "__main__":
    excuse_ok = test_excuse_generation()
    letter_ok = test_letter_generation()
    reply_ok = test_smart_reply()

    if excuse_ok and letter_ok and reply_ok:
        print("\nAll AI features verified successfully!")
    else:
        print("\nSome verification steps failed. Please check the responses above.")
