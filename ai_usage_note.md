# AI Usage Note

## How AI Was Used in This Project

1. **Architecture & Planning:** 
   AI was utilized to design the file structure, module separation, and component interactions, ensuring a clean separation of concerns between frontend, parsing, translation, and LLM interaction.

2. **Code Generation:**
   - AI generated the core logic for Streamlit components (`app.py`), styling, and layout to ensure a professional "enterprise tool" look.
   - The SQL parser (`sql_reader.py`) and dialect detector heuristics (`dialect_detector.py`) were developed with AI assistance.
   - The LLM integration (`llm_agent.py`) uses the `google-genai` SDK to fetch structured JSON, ensuring the output from the AI migration agent is strictly parsable.

3. **Prompts and Structuring:**
   AI helped design the strict JSON-only prompt used in `llm_agent.py` to ensure the migration agent's output could be programmatically read and displayed in the UI and downloaded as reports.

## Where AI Encountered Limitations (and How They Were Addressed)

1. **Complex Parser Logic:**
   Initially relying purely on LLMs for SQL translation can be slow and expensive. 
   **Solution:** We integrated `sqlglot` as the primary translation engine. The AI (LLM) is used as a fallback and an analytical tool. If `sqlglot` fails or encounters an unsupported construct, the error context is passed to the LLM to provide a reasoned, manual fix suggestion.

2. **JSON Formatting Issues:**
   LLMs sometimes wrap JSON in markdown backticks (e.g., ` ```json ... ``` `). 
   **Solution:** We used the Gemini API's `response_mime_type="application/json"` configuration to strictly enforce JSON output, reducing the need for complex regex extraction.

3. **Dialect Detection Certainty:**
   It is very difficult for simple heuristic code to perfectly guess the dialect of a generic `SELECT * FROM table;` statement.
   **Solution:** We built a fallback mechanism where `sqlglot` attempts to parse it with multiple dialects, but ultimately allow the user to manually select the source and target dialect in the Streamlit UI.
