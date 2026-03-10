# Smart Excuse & Letter Generator

A high-performance modern web application designed to instantly generate believable excuses and professional letters. Built with a Flask backend, PostgreSQL database on Neon, and a responsive HTML5/CSS3/JS frontend featuring a glassmorphism design.

## Features
- **Excuse Generator:** Provides context-aware excuse generation with believability scores and multiple variations.
- **Letter Generator:** Creates formally structured sick leaves, apology letters, and general permission letters with real-time typing animation previews.
- **Smart Templates:** Browse pre-built templates for quick selection and categorization.
- **User Dashboard & History:** Securely authenticate to save generated texts to your history and quickly reference or copy them later.
- **Instant Export:** Export your generated content to PDF (`pdfkit`) or Word documents (`python-docx`) instantly.
- **Dark/Light Themes:** Seamless visual transition utilizing global CSS variables with local storage persistence.
- **Responsive Animations:** Featuring typing effects, interactive hover states, and loading spinners.

## How it Works

The application operates fundamentally on a client-server architecture with dynamic rendering driven by JavaScript APIs connecting to a Python Flask backend.

### 1. The Frontend (Client-Side)
- **UI/UX Design**: The application UI is completely custom-built using HTML5 and CSS3 in a "Glassmorphism" style. Global colors are driven by CSS variables allow for a seamless Dark/Light mode toggle handled by `main.js`.
- **Interactivity (`excuses.js`, `letters.js`)**: Instead of relying on traditional form submissions that refresh the page, the frontend uses JavaScript `fetch()` to call the backend APIs asynchronously. 
- **Dynamic Feedback**: When generating a letter, a typing animation is triggered on the response chunk, providing a premium experience. Excuses return multiple variations which are dynamically mapped to a results container alongside a believability score.

### 2. The Backend (Server-Side)
- **Flask Framework**: The Python backend is structured using Flask Blueprints (`auth.py`, `excuses.py`, `letters.py`, `history.py`, `export.py`). This strictly separates the concerns of the application.
- **Generation Logic**: The core logic dynamically combines user inputs with pre-configured templates. For excuses, it randomly assigns varying reasons based on the selected "circumstance". For letters, it formally replaces template placeholders (like `[Recipient Name]`, `[Your Name]`) with the user's structured input.
- **Document Export**: The `/api/export/pdf` and `/api/export/docx` endpoints read the generated raw text from the frontend requests, format it into an HTML intermediary (for PDF via wkhtmltopdf) or use `python-docx` to generate files in-memory before sending them back as downloadable attachments.

### 3. The Database (PostgreSQL)
- **Neon Cloud DB**: The application connects securely to a PostgreSQL database hosted on Neon. 
- **Data Schemas**: 
  - `users`: Stores user accounts with hashed passwords using Werkzeug security.
  - `history`: Acts as the central table linking users to their generated excuses and letters via foreign keys.
  - `excuses` & `letters`: Store the actual generated text and metadata associated with user requests.
- **Authentication**: When a user logs in, Flask handles the session creation. This session determines if the backend will record the generated excuse/letter into the `history` table.

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.x, Flask (Blueprint Architecture)
- **Database**: PostgreSQL (Neon Cloud Platform)
- **Core Dependencies**: `psycopg2-binary` (database adapter), `pdfkit` (PDF generation), `python-docx` (Word generation), `Flask-Session`

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "Excuse Generator for Late Students"
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have `wkhtmltopdf` installed in your system PATH if you wish to use the PDF export functionality.*

3. **Configure Environment:**
   Create or review `.env`:
   ```env
   DATABASE_URL=postgresql://neondb_owner:...
   SECRET_KEY=your_secret_key
   ```

4. **Initialize the Database Schema:**
   *(Run this once to create your tables)*
   ```bash
   python backend/database/db.py
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be running locally at `http://127.0.0.1:5000`.

## Architecture Note
The application follows a modular MVC-like pattern layout where routes are cleanly separated in `backend/routes/`. The database logic strictly uses parameterized queries against the cloud database to prevent SQL injection vulnerabilities.
