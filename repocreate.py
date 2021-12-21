import json
import sys
import os
import requests
from pprint import pprint
import argparse

SSH_KEYS = ['personal', 'upt']
# Getting Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", type=str, dest="name", required=True)
parser.add_argument("--private", "-p", dest="is_private",
					action='store_true')
# sshkey = Host in .ssh config file
parser.add_argument("--sshkey", "-sk", type=str, dest="sshkey",
					required=True)
args = parser.parse_args()


def create_repo():
	repo_name = args.name
	is_private = args.is_private
	sshkey = args.sshkey
	if sshkey not in SSH_KEYS:
		raise Exception("Wrong argument for sshkey")

	if sshkey == 'personal':
		GITHUB_TOKEN = os.getenv("PersonalGitHubToken")
	elif sshkey == 'upt':
		GITHUB_TOKEN = os.getenv("UptGitHubToken")
	API_URL = "https://api.github.com"

	if is_private:
		payload = {
			"name": repo_name,
			"private": "true"
		}
	else:
		payload = {
			"name": repo_name,
			"private": "false"
		}
	headers = {
		"Authorization": "token " + GITHUB_TOKEN,
		"Accept": "application/vnd.github.v3+json"
	}
	try:
		r = requests.post(API_URL + "/user/repos", data=json.dumps(payload),
						  headers=headers)
		r.raise_for_status()
		pprint(r.json())
	except requests.exceptions.RequestException as err:
		raise SystemExit(err)


def clone_repo_locally():
	sshkey = args.sshkey
	if sshkey not in SSH_KEYS:
		raise Exception("Wrong argument for sshkey")
	try:
		if sshkey == 'personal':
			email = "piscoiandrei27@gmail.com"
			user = "piscoiandrei"
		elif sshkey == 'upt':
			email = "andrei.piscoi@student.upt.ro"
			user = "piscoiandreiupt"
		repo_name = args.name
		REPO_PATH = "D:/git" + sshkey + "/"
		CLONE_CMD = f"git clone git@{sshkey}:{user}/{repo_name}.git"
		os.chdir(REPO_PATH)
		os.system(CLONE_CMD)
		os.chdir(REPO_PATH + repo_name + '/')
		os.system(f"git config user.email {email}")
		os.system('echo About this project: > README.md')
		os.system("git add .")
		os.system('git commit -m "Initial Commit"')
		os.system("git push")
	except FileExistsError as err:
		raise SystemExit(err)


if __name__ == '__main__':
	print(args)
	create_repo()
	print("Remote repo created successfully")
	clone_repo_locally()
	print("Local repo created successfully")
