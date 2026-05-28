import subprocess
from constants import CORAL_CLI_COMMAND, FORMAT_TO_JSON

class NumberOfCommits():

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.sql_query = f"SELECT participation.all FROM github.participation WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.append(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if(result.stderr):
                return result.stderr
            else:
                return result.stdout
        except Exception as e:
            print(f"Error: {e}")