import subprocess

subprocess.run(['coral', 'sql', "SELECT author, commit__message FROM github.commits WHERE owner = 'kaveh0007' AND repo = 'flask-blog'"])