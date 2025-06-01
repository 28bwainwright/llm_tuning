# Model Tuning with Streamlit, SQLite Cloud, and Gemini

This Streamlit application provides a user-friendly interface for managing fine-tuning data for a Large Language Model (LLM) and interacting with the Gemini API. You can add, update, and delete question-answer pairs stored in a SQLite Cloud database, and also directly chat with the Gemini model.

---

## Features

* **Secure Access:** Requires API keys for both SQLite Cloud and Gemini to ensure secure operation.
* **Fine-Tune Data Management:**
    * **Add Records:** Easily add new question-answer pairs to your fine-tuning dataset.
    * **Edit Records:** Select an existing record to modify its question or answer.
    * **Delete Records:** Remove unwanted question-answer pairs from your dataset.
    * **Data Display:** View all your fine-tuning data in a clear, tabular format.
* **LLM Interaction:**
    * **Chat Interface:** Directly send prompts to the Gemini 2.0 Flash model and view its responses.
* **Persistent Storage:** Utilizes SQLite Cloud for reliable storage of your fine-tuning data.

---

## How to Run

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Make sure you have a `requirements.txt` file with `streamlit`, `sqlitecloud`, `polars`, and `google-generativeai` listed.)

3.  **Set Up API Keys:**

    This application uses `st.secrets` to securely store API keys. You'll need to create a `.streamlit/secrets.toml` file in your project directory with the following content:

    ```toml
    # .streamlit/secrets.toml
    db_key = "your_sqlitecloud_api_key"
    llm_key = "your_gemini_api_key"
    ```
    Replace `"your_sqlitecloud_api_key"` and `"your_gemini_api_key"` with your actual keys.

4.  **Run the Streamlit App:**
    ```bash
    streamlit run your_app_name.py
    ```
    (Replace `your_app_name.py` with the actual name of your Python script, likely `app.py` or `main.py` if you rename it.)

---

## Usage

Once the application is running, you'll see a web interface in your browser:

1.  **Sidebar Key Entry:** On the left sidebar, enter your SQLite Cloud database key and your Gemini API key in the respective input fields. **Note:** These keys are validated against your `secrets.toml` file.
2.  **Navigation Tabs:**
    * **Home:** Displays this README file.
    * **Fine Tune Data:** This tab allows you to manage your question-answer pairs:
        * The main area shows your existing data. Select a row to populate the editing form on the right.
        * **Add New:** Fill in the "Question" and "Answer" fields and click "Submit."
        * **Update Existing:** Select a row, modify the "Question" or "Answer" fields, and click "Update."
        * **Delete Record:** Select a row and click "Delete."
    * **Chat:** Use this tab to interact directly with the Gemini model. Type your question in the input box and click "Ask." The model's response will be displayed below.
    * **Overview:** (Currently displays a placeholder; you can expand this section with more information later.)

---

## Database Schema

The application expects a table named `fine_tuned_christian` in your SQLite Cloud database with the following schema:

```sql
CREATE TABLE fine_tuned_christian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
```

---

## Technologies Used

* **Streamlit:** For building the interactive web application.
* **SQLite Cloud:** For cloud-hosted, persistent storage of fine-tuning data.
* **Polars:** For efficient data manipulation and display (specifically `pl.read_database`).
* **Google Generative AI (Gemini API):** For interacting with the Gemini 2.0 Flash language model.

---

## Future Enhancements (Ideas)

* Implement user authentication and authorization.
* Add more sophisticated data filtering and searching capabilities for the fine-tuning data.
* Integrate model fine-tuning directly within the application (e.g., triggering a fine-tuning job).
* Provide more detailed model tuning metrics and analytics.
* Allow users to select different Gemini models or parameters.
* Enhance error handling and user feedback.
