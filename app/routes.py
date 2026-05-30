from app import app, client
from app.forms import IssueForm
from app.models.schema import SQLQueryFromGenAI
from app.constants import GEMINI_MODEL
from flask import render_template, abort
from google.genai import types
from app.prompts import SYSTEM_INSTRUCTION_FIRST_PASS
import json
from app.queries import CLASS_MAP

@app.route("/", methods=["GET", "POST"])
def home():
    form = IssueForm()
    if form.validate_on_submit():
        user_query = form.issue.data + "Owner_Name: "
        if form.owner_name.data:
            user_query += " owner_name: " + form.owner_name.data
        if form.repository_name.data:
            user_query += " repository_name: " + form.repository_name.data
        print(user_query)
        response = client.models.generate_content(
            model = GEMINI_MODEL,
            contents = user_query,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
                response_json_schema = SQLQueryFromGenAI.model_json_schema(),
                system_instruction = SYSTEM_INSTRUCTION_FIRST_PASS
            ),
        )
        payload = json.loads(response.text)
        print(payload.get("thinking_process"))
        if payload.get("is_possible_via_templates"):
            if payload.get("missing_attributes"):
                abort(400)
            else:
                if payload.get("query_template_class") in CLASS_MAP:
                    query_template_class = CLASS_MAP[payload.get("query_template_class")]
                    query_instance = query_template_class(**payload.get("attributes"))
                    result = query_instance.execute_query()
                    print(result)
                else:
                    print("We are having some issues try again later")
        else:
            print("Trying Coral MCP and making the LLM create the query")
        return "Placeholder"
    return render_template("home.html", form=form)

@app.errorhandler(503)
def handle_503_error(error):
    return render_template("errors/503_error.html", title="503 Error"), 503

@app.errorhandler(400)
def handle_400_error(error):
    return render_template("errors/400_error.html", title="Insufficient Information"), 400