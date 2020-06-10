#!/usr/bin/env python

import shlex
import subprocess
import requests
import os


def get_workflow_id():

    branch_name = subprocess.check_output(shlex.split('git rev-parse --abbrev-ref HEAD')).strip().decode("utf-8")
    circle_token = os.getenv('CIRCLE_CI_TOKEN')
    project = os.getenv('CIRCLE_CI_PROJECT')

    url = 'https://circleci.com/api/v1.1/project/{}/tree/{}?circle-token={}'.format(
        project,
        branch_name,
        circle_token,
    )
    r = requests.get(url)
    jobs_list = r.json()

    for job in jobs_list:
        if job.get('workflows', {}).get('workflow_name') == 'tests':
            return job['workflows']['workflow_id']


if __name__ == '__main__':
    workflow_id = get_workflow_id()
    workflow_url = 'https://circleci.com/workflow-run/{}'.format(workflow_id)
    subprocess.call(['open', workflow_url])
