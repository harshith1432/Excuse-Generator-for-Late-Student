import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from backend.ai_client import ai_client

def test_formatted_letter_generation():
    print("Testing Professional Letter Generation...")
    details = {
        "recipient_name": "Dr. Smith",
        "subject": "Research Grant Inquiry",
        "reason": "Requesting information about available grants for AI research in 2026.",
        "name": "Harshith D",
        "college_company": "Jain University",
        "type": "Inquiry Letter"
    }
    
    # Simulate the prompt building logic
    import datetime
    prompt = (
        "Write a professional formal letter/application based on these details:\n"
        f"- Recipient: {details['recipient_name']}\n"
        f"- Subject: {details['subject']}\n"
        f"- Reason/Context: {details['reason']}\n"
        f"- Sender Name: {details['name']}\n"
        f"- Sender Credentials: {details['college_company']}\n"
        f"- Date: {datetime.date.today().strftime('%B %d, %Y')}\n\n"
        "The letter MUST follow this EXACT structure:\n"
        "1. FROM ADDRESS: Sender Name and Credentials at the top.\n"
        "2. DATE: Current date.\n"
        "3. TO ADDRESS: Recipient details.\n"
        "4. SUBJECT: Clear 'Subject:' line.\n"
        "5. SALUTATION: Professional greeting (e.g., Respected Sir/Madam or Dear [Name]).\n"
        "6. BODY: Well-structured paragraphs addressing the reason.\n"
        "7. CLOSING: Professional sign-off (e.g., Thanking you, Best regards) followed by Sender Name.\n\n"
        "Return ONLY the formatted letter content. Do not include any extra text."
    )
    
    response = ai_client.generate_text(prompt)
    print(f"Generated Letter:\n{response}")
    
    # Check for structural patterns
    checks = {
        "Sender Info": "Harshith" in response or "Jain University" in response,
        "Date": datetime.date.today().strftime('%B %d, %Y') in response,
        "Recipient": "Smith" in response,
        "Subject Line": "Subject:" in response,
        "Salutation": "Dear" in response or "Respected" in response,
        "Closing": "Best regards" in response or "Sincerely" in response or "Thanking you" in response
    }
    
    for check, passed in checks.items():
        print(f"[{'PASSED' if passed else 'FAILED'}] {check}")
    
    return all(checks.values()), response

def test_pdf_export(content):
    print("\nTesting PDF Export with fpdf2...")
    from fpdf import FPDF
    import tempfile
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=safe_content)
        
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "test_letter.pdf")
        pdf.output(temp_path)
        
        size = os.path.getsize(temp_path)
        print(f"PDF generated at: {temp_path} (Size: {size} bytes)")
        return size > 0
    except Exception as e:
        print(f"PDF Export Failed: {e}")
        return False

if __name__ == "__main__":
    letter_ok, content = test_formatted_letter_generation()
    if letter_ok:
        pdf_ok = test_pdf_export(content)
        if pdf_ok:
            print("\nFormatting and PDF verification successful!")
        else:
            print("\nPDF verification failed.")
    else:
        print("\nLetter formatting verification failed.")
