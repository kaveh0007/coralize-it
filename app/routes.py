from app import app, client
from app.forms import IssueForm
from app.models.schema import SQLQueryFromGenAI
from app.constants import SYSTEM_INSTRUCTION, GEMINI_MODEL, CORAL_CLI_COMMAND
from app.utils import query_coral_schema
from flask import render_template
from google.genai import types
import subprocess

# tools = types.Tool(function_declarations=[query_coral_schema])

@app.route("/", methods=["GET", "POST"])
def home():
    form = IssueForm()
    if form.validate_on_submit():
        print(1111)
        user_query = form.issue.data
        response = client.models.generate_content(
            model = GEMINI_MODEL,
            contents = user_query,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
                response_schema = SQLQueryFromGenAI,
                system_instruction = SYSTEM_INSTRUCTION,
                tools = [types.Tool(function_declarations=[query_coral_schema])]
            ),
        )
        print(response.text)
        command = CORAL_CLI_COMMAND.copy()
        command.append(response.text)
        result = subprocess.run(command, capture_output=True, text=True)
        print(result)
        return "Placeholder"
    return render_template("home.html", form=form)