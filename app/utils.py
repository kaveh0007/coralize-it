from app.constants import CORAL_CLI_COMMAND, FORMAT_TO_JSON
import subprocess


def query_coral_schema(table_name):
    query = f"SELECT table_name, description, required_filters, guide FROM coral.tables where coral.tables.schema_name = {table_name}"

    cli_command = CORAL_CLI_COMMAND.copy()
    cli_command.append(query)
    cli_command.extend(FORMAT_TO_JSON)

    try:
        response = subprocess.run(
            cli_command, capture_output=True, check=True, text=True
        )
        return response.stdout
    except Exception as e:
        return "Error retrieving the schema set is_possible to false and do not return any sql"
