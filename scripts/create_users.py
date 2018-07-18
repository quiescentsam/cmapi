#!/usr/bin/python

from collections import namedtuple
from cm_api.api_client import ApiResource
from cm_api.api_client import API_CURRENT_VERSION
from cm_api.endpoints.types import ApiCommand
from cm_api.api_client import ApiException
from threading import Thread
from urlparse import urlparse
import argparse
import os
import sys
import time

class CommandWait(Thread):
    """
    A class that will wait on a command indefinitely.
    """

    def __init__(self, command):
        Thread.__init__(self)
        self.command = command

    def run(self):
        self.command.wait()

def retrieve_args():
    """
    Attempts to retrieve Cloudera Manager connection information from the environment.
    If that fails, the information is parsed from the command line.
    @rtype:  namespace
    @return: The parsed arguments.
    """

    if all(env_var in os.environ for env_var in ("DEPLOYMENT_HOST_PORT",
                                                 "CM_USERNAME", "CM_PASSWORD",
                                                 "CLUSTER_NAME")):
        write_to_stdout("Arguments detected in environment -- command line arguments being ignored.\n")
        args = namedtuple("args", ["host", "port", "username", "password", "cluster", "use_tls"])

        parsed_url = os.environ["DEPLOYMENT_HOST_PORT"].split(":")
        args.host = parsed_url[0]
        args.port = int(parsed_url[1])
        args.username = os.environ["CM_USERNAME"]
        args.password = os.environ["CM_PASSWORD"]
        args.cluster = os.environ["CLUSTER_NAME"]
        args.use_tls = False

        return args
    else:
        return parse_args()

def parse_args():
    """
    Parses host and cluster information from the given command line arguments.
    @rtype:  namespace
    @return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Configure an existing cluster",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('host', metavar='HOST', type=str, help="The Cloudera Manager host")
    parser.add_argument('cluster', metavar='CLUSTER', type=str,
                        help="The name of the cluster to kerberize")
    parser.add_argument('--port', metavar='port', type=int, default=7180,
                        help="Cloudera Manager's port.")
    parser.add_argument('--username', metavar='USERNAME', type=str, default='admin',
                        help="The username to log into Cloudera Manager with.")
    parser.add_argument('--password', metavar='PASSWORD', type=str, default='admin',
                        help="The password to log into Cloudera Manager with.")
    parser.add_argument('--use-tls', action='store_true',
                        help="Whether to use TLS to connect to Cloudera Manager.")
    return parser.parse_args()




def manage_cm_users(api):
    try:
        api.create_user('nielsen', 'nielsen#123', ['ROLE_USER'])
    except ApiException as e:
        if '0 insert' in str(e):
            print 'user created already'
        else:
            raise e

def write_to_stdout(msg):
    """
    Utility command to write to stdout and immediately flush.
    @type  msg: str
    @param msg: The message to write to stdout.
    """
    sys.stdout.write(msg)
    sys.stdout.flush()

def main():
    """
    Configures a cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = retrieve_args()

    api = ApiResource(settings.host, settings.port, settings.username,
                      settings.password, settings.use_tls, 8)

    cluster = api.get_cluster(settings.cluster)

    #manage_cm_users(api)
    users=['test1','test2']
    for user in users:
        print user
        api.create_user(user, 'nielsen#123', ['ROLE_USER'])


    return 0

if __name__ == '__main__':
    sys.exit(main())

