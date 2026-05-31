from app import app, client
from app.forms import IssueForm
from app.models.schema import QueryTemplateClassFromGenAI, GenAIResponseToUser
from app.constants import GEMINI_MODEL, NOT_POSSIBLE_VIA_TEMPLATES
from flask import render_template, abort, jsonify
from google.genai import types
from app.prompts import SYSTEM_INSTRUCTION_FIRST_PASS, SYSTEM_INSTUCTION_SECOND_PASS
import json
from app.queries import CLASS_MAP
from google.genai.errors import ClientError
from pathlib import Path

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
        try:
            response = client.models.generate_content(
                model = GEMINI_MODEL,
                contents = user_query,
                config = types.GenerateContentConfig(
                    response_mime_type = "application/json",
                    response_json_schema = QueryTemplateClassFromGenAI.model_json_schema(),
                    system_instruction = SYSTEM_INSTRUCTION_FIRST_PASS
                )
            )
        except ClientError as e:
            if e.code == 429:
                abort(429)
            raise
        payload = json.loads(response.text)
        print(payload)
        if payload.get("is_possible_via_templates"):
            if payload.get("missing_attributes"):
                abort(400)
            else:
                if payload.get("query_template_class") in CLASS_MAP:
                    query_template_class = CLASS_MAP[payload.get("query_template_class")]
                    query_instance = query_template_class(**payload.get("attributes"))
                    result = query_instance.execute_query()
                else:
                    abort(500)
        else:
            result = NOT_POSSIBLE_VIA_TEMPLATES
        
        query_and_raw_response = f"Query was: {user_query} and the raw response is: {result}" 
        print(query_and_raw_response)
        try:
            response = client.models.generate_content(
                model = GEMINI_MODEL,
                contents = query_and_raw_response,
                config = types.GenerateContentConfig(
                    response_mime_type = "application/json",
                    response_json_schema = GenAIResponseToUser.model_json_schema(),
                    system_instruction = SYSTEM_INSTUCTION_SECOND_PASS
                )
            )
        except ClientError as e:
            if e.code == 429:
                abort(429)
            raise

        payload = json.loads(response.text)

        if payload.get("response_to_user"):
            flag = True
        return render_template("home.html", form=form, flag=flag, response=payload.get("response_to_user"))
    return render_template("home.html", form=form, flag=flag)

@app.route("/api/mocks", methods=["GET"])
def get_mocks():
    try:
        mocks_path = Path(__file__).absolute().parents[1] / "mocks.json"
        with open(mocks_path, "r") as f:
            mocks = json.load(f)
        return jsonify(mocks)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

@app.errorhandler(503)
def handle_503_error(error):
    return render_template("errors/503_error.html", title="Service Unavailable"), 503

@app.errorhandler(400)
def handle_400_error(error):
    return render_template("errors/400_error.html", title="Insufficient Information"), 400

@app.errorhandler(500)
def handle_500_error(error):
    return render_template("errors/500_error.html", title="Its on us"), 500

@app.errorhandler(429)
def handle_error(error):
    return render_template("errors/429_error.html", title="Resource Exhausted"), 429