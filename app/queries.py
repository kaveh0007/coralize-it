import subprocess
import json
from app.constants import CORAL_CLI_COMMAND, FORMAT_TO_JSON

class NumberOfCommits():
    """Get weekly commit count for a specific week in the last 52 weeks"""
    def __init__(self, owner, repo, week_index):
        self.owner = owner
        self.repo = repo
        self.week_index = week_index
        self.sql_query = f"SELECT participation.all FROM github.participation WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            weekly_commits = json.loads(response[0].get("all"))
            return {"week_index": self.week_index, "commits": weekly_commits[self.week_index]}
        except Exception as e:
            return {"error": str(e)}

class CommitFrequency():
    """Get total and average commit frequency for a repository"""
    
    def __init__(self, owner, repo, time_period="1 year"):
        self.owner = owner
        self.repo = repo
        self.time_period = time_period
        self.sql_query = f"SELECT * FROM github.commit_activity WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            return {"total_weeks": len(response), "commit_activity": response}
        except Exception as e:
            return {"error": str(e)}

class CodeFrequency():
    """Get weekly additions and deletions (code churn)"""
    
    def __init__(self, owner, repo, week_offset=0):
        self.owner = owner
        self.repo = repo
        self.week_offset = week_offset
        self.sql_query = f"SELECT * FROM github.code_frequency WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            
            response = json.loads(result.stdout)   
            json_data = response[0].get("json")
            if not json_data:
                return {"error": "Data unavailable", "reason": "GitHub API returned no code frequency data. This typically occurs for repos with >1000 commits or inactive repos."}
            
            data_list = json_data if isinstance(json_data, list) else [json_data]
            return {"code_frequency_data": data_list[:10]}
        
        except Exception as e:
            return {"error": str(e)}

class TopContributors():
    """Get top contributors to repository"""
    
    def __init__(self, owner, repo, limit=10):
        self.owner = owner
        self.repo = repo
        self.limit = int(limit)
        self.sql_query = f"SELECT author FROM github.commits WHERE owner='{owner}' AND repo='{repo}' LIMIT {int(limit)}"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            return {"contributors": response}
        except Exception as e:
            return {"error": str(e)}
        
class CheckRunStatus():
    """Get CI/CD check run success rate"""
    
    def __init__(self, owner, repo, ref):
        self.owner = owner
        self.repo = repo
        self.ref = ref
        self.sql_query = f"SELECT status, conclusion FROM github.check_runs WHERE owner='{owner}' AND repo='{repo}' AND ref='{ref}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            if not response:
                return {"error": "No check runs found", "reason": f"No check runs available for ref '{self.ref}'"}
            total = len(response)
            success = sum(1 for r in response if r.get("conclusion") == "success")
            return {"total_runs": total, "successful_runs": success, "success_rate": f"{(success/total*100):.2f}%" if total > 0 else "0%"}
        except Exception as e:
            return {"error": str(e)}

class RepositoryActivity():
    """Get recent repository activity"""
    
    def __init__(self, owner, repo, limit):
        self.owner = owner
        self.repo = repo
        self.limit = limit
        self.sql_query = f"SELECT * FROM github.activity WHERE owner='{owner}' AND repo='{repo}' LIMIT {int(limit)}"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            if not response:
                return {"error": "No recent activity", "reason": "Repository has no recent activity"}
            return {"recent_activities": response}
        except Exception as e:
            return {"error": str(e)}

class IssueResolutionMetrics():
    """Get issue creation and resolution metrics"""
    
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.sql_query = f"SELECT state FROM github.issues WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            open_issues = sum(1 for r in response if r.get("state") == "open")
            closed_issues = sum(1 for r in response if r.get("state") == "closed")
            total_issues = len(response)
            return {"total_issues": total_issues, "open_issues": open_issues, "closed_issues": closed_issues}
        except Exception as e:
            return {"error": str(e)}
        
class LatestIssueAndHint():
    """Get analysis on how to solve the latest issue that's open"""
    
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.sql_query = f"SELECT * FROM github.issues WHERE owner='{owner}' AND repo='{repo}' AND state='open' LIMIT 1"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            return response
        except Exception as e:
            return {"error": str(e)}

class PullRequestMetrics():
    """Get pull request activity and status for the most recent pull"""
    
    def __init__(self, owner, repo, state="all"):
        self.owner = owner
        self.repo = repo
        self.state = state
        self.sql_query = f"SELECT * FROM github.pulls WHERE owner='{owner}' AND repo='{repo}'"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            open_prs = sum(1 for r in response if r.get("state") == "open")
            merged_prs = sum(1 for r in response if r.get("merged"))
            return {"total_prs": len(response), "open_prs": open_prs, "merged_prs": merged_prs}
        except Exception as e:
            return {"error": str(e)}

class ReviewActivityMetrics():
    """Get code review metrics"""
    
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.sql_query = f"SELECT * FROM github.reviews WHERE owner='{owner}' AND repo='{repo}' LIMIT 100"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            approved = sum(1 for r in response if r.get("state") == "APPROVED")
            requested_changes = sum(1 for r in response if r.get("state") == "CHANGES_REQUESTED")
            return {"total_reviews": len(response), "approved": approved, "changes_requested": requested_changes}
        except Exception as e:
            return {"error": str(e)}

class CommitMetrics():
    """Get commit related metrics"""
    
    def __init__(self, owner, repo, limit=50):
        self.owner = owner
        self.repo = repo
        self.limit = limit
        self.sql_query = f"SELECT * FROM github.commits WHERE owner='{owner}' AND repo='{repo}' LIMIT {limit}"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            return {"recent_commits": response}
        except Exception as e:
            return {"error": str(e)}
        
class DeploymentMetrics():
    """Get deployment frequency and status"""
    
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.sql_query = f"SELECT * FROM github.deployments WHERE owner='{owner}' AND repo='{repo}' LIMIT 50"
    
    def execute_query(self):
        command = CORAL_CLI_COMMAND.copy()
        command.append(self.sql_query)
        command.extend(FORMAT_TO_JSON)
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            if result.stderr:
                return {"error": result.stderr}
            response = json.loads(result.stdout)
            return {"total_deployments": len(response), "recent_deployments": response[:10]}
        except Exception as e:
            return {"error": str(e)}

CLASS_MAP = {
    "NumberOfCommits": NumberOfCommits,
    "CommitFrequency": CommitFrequency,
    "CodeFrequency": CodeFrequency,
    "TopContributors": TopContributors,
    "CheckRunStatus": CheckRunStatus,
    "RepositoryActivity": RepositoryActivity,
    "IssueResolutionMetrics": IssueResolutionMetrics,
    "LatestIssueAndHint": LatestIssueAndHint,
    "PullRequestMetrics": PullRequestMetrics,
    "ReviewActivityMetrics": ReviewActivityMetrics,
    "CommitMetrics": CommitMetrics,
    "DeploymentMetrics": DeploymentMetrics
}