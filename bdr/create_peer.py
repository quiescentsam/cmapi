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
    Configures a cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = retrieve_args()

    #api = ApiResource(settings.host, settings.port, settings.username,
    #                  settings.password, settings.use_tls, 8)

    #cluster = api.get_cluster(settings.cluster)

    TARGET_CM_HOST = "<destination_cluster>"
    SOURCE_CM_URL = "<source_cluster>:7180/"

    api_root = ApiResource(TARGET_CM_HOST, username="<username>", password="<password>")
    cm = api_root.get_cloudera_manager()
    cm.create_peer("peer1", SOURCE_CM_URL, '<username>', '<password>')


    return 0

if __name__ == '__main__':
    sys.exit(main())



