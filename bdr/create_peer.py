#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *
import argparse
import os
import sys
from collections import namedtuple


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
        sys.stdout.write("Arguments detected in environment -- command line arguments being ignored.\n")
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



def main():
    """
    Add peer to the cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = retrieve_args()


    TARGET_CM_HOST = "18.205.59.216"
    SOURCE_CM_URL = "http://34.226.244.149:7180/"


    api_target = ApiResource(settings.host, settings.port, settings.username,
                      settings.password, settings.use_tls, 14)

    api_root = ApiResource(TARGET_CM_HOST, username="admin", password="admin")
    cm = api_target.get_cloudera_manager()
    cm.create_peer("peer1", SOURCE_CM_URL, 'admin', 'admin')


    return 0

if __name__ == '__main__':
    sys.exit(main())



