#!/usr/bin/env python3

import argparse
import json
import logging
import os
import requests
import sys
import textwrap
import time


class Logger:

    class Formatter(logging.Formatter):
        FORMATS = {
            logging.INFO: '[\033[32;1m%(levelname)s\033[0m] %(asctime)s - (%(filename)s:%(lineno)d) - %(message)s',
            logging.WARNING: '[\033[33;1m%(levelname)s\033[0m] %(asctime)s - (%(filename)s:%(lineno)d) - %(message)s',
            logging.ERROR: '[\033[31;1m%(levelname)s\033[0m] %(asctime)s - (%(filename)s:%(lineno)d) - %(message)s',
        }


        def format(self, record):
            format = self.FORMATS.get(record.levelno,
                                 '[%(levelname)s] %(asctime)s - (%(filename)s:%(lineno)d) - %(message)s')
            formatter = logging.Formatter(format, datefmt='%Y-%m-%d %H:%M:%S')
            return formatter.format(record)


    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = self.Formatter()
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)


class CirrusCI:

    def __init__(self, token, repository, branch):
        self.token = token
        self.repository = repository
        self.branch = branch
        self.url = 'https://api.cirrus-ci.com/graphql'


    def request(self, query, variables, token=None):
        payload = {
            'query'     : textwrap.dedent(query).strip(),
            'variables' : variables,
        }
        headers = {} if token is None else {'Authorization' : 'Bearer {}'.format(token)}
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()


    def get_repository_id(self):
        owner, name = self.repository.split('/')
        query = '''
            query GetRepositoryID($owner: String!, $name: String!) {
                ownerRepository(platform: "github", owner: $owner, name: $name) {
                    id
                }
            }
        '''
        variables = {'owner': owner, 'name': name}
        response = self.request(query, variables)
        owner_repository = response['data']['ownerRepository']
        if owner_repository is None:
            raise RuntimeError(response)
        return owner_repository['id']


    def create_build(self, repository_id):
        query = '''
            mutation CreateBuild($repository_id: ID!, $branch: String!, $mutation_id: String!) {
                createBuild(input: {
                    repositoryId: $repository_id,
                    branch: $branch,
                    clientMutationId: $mutation_id
                }) {
                    build {
                        id,
                        status
                    }
                }
            }
        '''
        variables = {
            'repository_id': repository_id,
            'branch': self.branch,
            'mutation_id': 'Cirrus-CI build ({})'.format(time.asctime())
        }
        response = self.request(query, variables, self.token)
        create_build = response['data']['createBuild']
        if create_build is None:
            raise RuntimeError(response)

        build_info = create_build['build']
        build_id, status = build_info['id'], build_info['status']
        if status != 'CREATED':
            raise RuntimeError('Failed to create build, status={}'.format(status))
        return build_id


    def wait_build(self, build_id, timeout=None, interval=None):
        query = '''
            subscription QueryBuild($build_id: ID!) {
                build(id: $build_id) {
                    status
                }
            }
        '''
        variables = {'build_id': build_id}

        timeout = 2 * 60 if timeout is None else timeout
        interval = 10 if interval is None else interval

        start_time = time.time()
        while (time.time() - start_time) / 60 < timeout:
            try:
                response = self.request(query, variables)
            except Exception as e:
                logger.warning(str(e))
                time.sleep(interval * 2)
                continue

            build = response['data']['build']
            if build is None:
                raise RuntimeError(response)
            status = build['status']
            logger.info('Check the status of the build, build_id={}, status={}, elapsed={}s'.format(
                            build_id, status, round(time.time() - start_time, 2)))
            if status not in ['CREATED', 'TRIGGERED', 'EXECUTING']:
                return status
            time.sleep(interval)


    def get_task_ids(self, build_id):
        query = '''
            query QueryBuild($build_id: ID!) {
                build(id: $build_id) {
                    tasks {
                        id
                    }
                }
            }
        '''
        variables = {'build_id': build_id}
        response = self.request(query, variables)
        build = response['data']['build']
        if build is None:
            raise RuntimeError(response)
        return [task['id'] for task in build['tasks']]


def trigger(arguments):
    ci = CirrusCI(arguments.token, arguments.repository, arguments.branch)

    repository_id = ci.get_repository_id()
    logger.info('The ID of repository {} is {}'.format(ci.repository, repository_id))

    build_id = ci.create_build(repository_id)
    logger.info('Create the Cirrus-CI build successfully, build_id={}'.format(build_id))

    status = ci.wait_build(build_id, arguments.timeout, arguments.interval)
    if status != 'COMPLETED':
        exit(1)

    task_ids = ci.get_task_ids(build_id)
    logger.info('The task IDs of build {} is {}'.format(build_id, task_ids))

    for task_id in task_ids:
        artifact_url = 'https://api.cirrus-ci.com/v1/artifact/task/{}/binary.zip'.format(task_id)
        logger.info('The url of the artifact is {}'.format(artifact_url))
        print(artifact_url)


logger = Logger().logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))
    parser.add_argument('-t', '--token', help='Cirrus-CI TOKEN', required=True)
    parser.add_argument('-r', '--repository', help='GitHub repository', required=True)
    parser.add_argument('-b', '--branch', help='The branch of the repository', required=True)
    parser.add_argument('-T', '--timeout', help='Timeout (in minutes)')
    parser.add_argument('-i', '--interval', help='Sleep interval (in seconds)')
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit(128)

    trigger(args)
