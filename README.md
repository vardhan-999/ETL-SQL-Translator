# ETL SQL Translator

An AI-powered SQL migration assistant designed to convert database schemas and queries between different SQL dialects (MySQL, PostgreSQL, SQLite).

## Architecture

1. **SQL File Upload:** Streamlit UI for user interaction.
2. **Dialect Detector:** Identifies the source dialect.
3. **SQL Translator:** Utilizes `sqlglot` for syntax-level translation.
4. **LLM Agent:** Employs the Gemini API to handle complex, unsupported conversions and generate JSON recommendations.
5. **Validator:** Validates the translated SQL against the target dialect parser.
6. **Report Generator:** Produces Markdown reports and JSON issue files.
7. **Database Logger:** Tracks migration history in an SQLite database.

## Features
- Translate between MySQL, PostgreSQL, and SQLite.
- AI-assisted manual fix suggestions.
- Validation checks for parsed queries.
- Dashboard for viewing migration history.
- Downloadable reports.

## Installation

1. Clone the repository and navigate to the root directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env` (or just edit `.env` if created).
   - Add your `GEMINI_API_KEY`.

## Execution

Run the Streamlit app:
```bash
streamlit run app.py
```

## AI Workflow
- The app uses `sqlglot` for initial translation.
- If `sqlglot` raises Parse or Transpile errors, or if specific keywords are flagged, the query and error context are sent to the LLM.
- The LLM acts as an expert migration engineer, returning structured JSON with issues detected and manual fix recommendations.

## Future Improvements
- Support for more complex schema translations (e.g., triggers, stored procedures).
- Integration with more databases (e.g., Oracle, SQL Server).
- Live execution of translated queries against a target database.
