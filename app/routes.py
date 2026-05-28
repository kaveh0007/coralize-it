from app import app, client
from app.forms import IssueForm
from app.models.schema import SQLQueryFromGenAI
from app.constants import GEMINI_MODEL
from flask import render_template
from google.genai import types
from app.prompts import SYSTEM_INSTRUCTION_FIRST_PASS

@app.route("/", methods=["GET", "POST"])
def home():
    form = IssueForm()
    if form.validate_on_submit():
        user_query = form.issue.data + "Owner_name: " + form.owner_name.data + " Repo Name: " + form.repository_name.data
        response = client.models.generate_content(
            model = GEMINI_MODEL,
            contents = user_query,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
                response_json_schema = SQLQueryFromGenAI.model_json_schema(),
                system_instruction = SYSTEM_INSTRUCTION_FIRST_PASS
            ),
        )
        print(response.text)
        return "Placeholder"
    return render_template("home.html", form=form)