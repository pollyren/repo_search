#!/usr/bin/env python3

import requests
import sys
import wget
from urllib.request import urlopen

file_name = sys.argv[1]

file = open(f'output/{file_name}', 'r')

file_contents = {}
repos = []
for line in file.readlines():
    try:
        repo_name, repo_path = line.strip().split(' ', 1)
        repo_path = repo_path.replace(' ', '%20')
    except:
        print(f'unable to split line: {line}')
        continue

    try:
        link = f'https://raw.githubusercontent.com/{repo_name}/main/{repo_path}'
        if requests.get(link).status_code > 400:
            link = f'https://raw.githubusercontent.com/{repo_name}/master/{repo_path}'
            if requests.get(link).status_code > 400:
                continue
        repo_fn = f'{repo_name}/{repo_path}'.replace('/','_')
        wget.download(link, 'repos/'+repo_fn)
        repos.append((repo_fn, repo_name, repo_path))
    except:
        continue

with open('repos/repos.txt', 'a') as f:
    for repo in repos:
        f.write(str(repo) + '\n')