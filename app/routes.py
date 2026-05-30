from app import app, client
from app.forms import IssueForm
from app.models.schema import SQLQueryFromGenAI, GenAIResponseToUser
from app.constants import GEMINI_MODEL
from flask import render_template, abort
from google.genai import types
from app.prompts import SYSTEM_INSTRUCTION_FIRST_PASS, SYSTEM_INSTUCTION_SECOND_PASS
import json
from app.queries import CLASS_MAP

@app.route("/", methods=["GET", "POST"])
def home():
    flag = False
    form = IssueForm()
    if form.validate_on_submit():
        user_query = form.issue.data
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
            )
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
                    abort(500)
        else:
            print("Trying Coral MCP and making the LLM create the query")
            # Fallback MCP Client logic will be added here
        
        query_and_raw_response = f"Query was: {user_query} and the raw response is: {result}" 
        response = client.models.generate_content(
            model = GEMINI_MODEL,
            contents = query_and_raw_response,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
                response_json_schema = GenAIResponseToUser.model_json_schema(),
                system_instruction = SYSTEM_INSTUCTION_SECOND_PASS
            )
        )

        payload = json.loads(response.text)

        if payload.get("response_to_user"):
            flag = True
        return render_template("home.html", form=form, flag=flag, response=payload.get("response_to_user"))
    return render_template("home.html", form=form, flag=flag)

@app.errorhandler(503)
def handle_503_error(error):
    return render_template("errors/503_error.html", title="Service Unavailable"), 503

@app.errorhandler(400)
def handle_400_error(error):
    return render_template("errors/400_error.html", title="Insufficient Information"), 400

@app.errorhandler(500)
def handle_500_error(error):
    return render_template("errors/500_error.html", title="Its on us"), 500