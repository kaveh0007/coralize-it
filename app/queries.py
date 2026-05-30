import subprocess
import json
from app.constants import CORAL_CLI_COMMAND, FORMAT_TO_JSON

class NumberOfCommits():

    def __init__(self, owner, repo, week_index):
        self.owner = owner
        self.repo = repo
        self.week_index = week_index
        self.sql_query = f"SELECT participation.all FROM github.participation WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        print("Inside the function: " + self.sql_query)
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if(result.stderr):
                return {"Error": result.stderr}
            else:
                response = json.loads(result.stdout)
                weekly_commits = json.loads(response[0].get("all"))
                return weekly_commits[self.week_index]
        except Exception as e:
            return {"Error": str(e)}

CLASS_MAP = {
    "NumberOfCommits" : NumberOfCommits
}