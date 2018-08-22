#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *
from cm_api.api_client import ApiException
import argparse
import os
import sys
from collections import namedtuple


def parse_args():
    """
    Parses host and cluster information from the given command line arguments.
    @rtype:  namespace
    @return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Adding Source cluster as 'peer' in Destination Cloudera Manager ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--host', metavar='HOST', type=str, help="The Cloudera Manager host")
    parser.add_argument('--port', metavar='port', type=int, default=7180, help="Cloudera Manager's port.")
    parser.add_argument('--username', metavar='USERNAME', type=str, default='admin',
                        help="The username to log into Cloudera Manager with.")
    parser.add_argument('--password', metavar='PASSWORD', type=str, default='admin',
                        help="The password to log into Cloudera Manager with.")
    parser.add_argument('--use-tls', action='store_true', help="Whether to use TLS to connect to Cloudera Manager.")
    parser.add_argument('--source_cm_url', metavar='Source Cloudera Manager URL', type=str, help="Full CM URL of the source cluster ie. https://hostname:7183/")
    parser.add_argument("--source-user", metavar='Source Cloudera Manager Username', type=str, default='admin',
                        help="The username to log into Source Cloudera Manager with." )
    parser.add_argument("--source-password", metavar='SOURCE_CM_PWD', type=str, default='admin',
                        help="The password to log into Source Cloudera Manager with." )
    parser.add_argument("--peer-name" , metavar='PEER_NAME', type=str, default='peer1',
                        help="ALias Name to be created of the Source cluster" )
    return parser.parse_args()


def print_usage_message():
    print ("Usage: python add_peer.py")
    print ("Example that lists queries that have run more than 10 minutes:")
    print ("python add_peer.py --host 18.205.59.216 --port 7180 --username admin --password admin "
           "--source_cm_url http://34.226.244.149:7180/ --source-user admin --source-password admin --peer-name peer2")
    print ("Example that creates peer with name peer2")



def main():
    """
    Add peer to the cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = parse_args()
    print len(sys.argv)
    # if len(sys.argv) == 1 or len(sys.argv) > 17:
    #     print_usage_message()
    # quit(1)

    # TARGET_CM_HOST = "18.205.59.216"
    # SOURCE_CM_URL = "http://34.226.244.149:7180/"
    print "came here 1"
    api_target = ApiResource(settings.host, settings.port, settings.username,settings.password, settings.use_tls, 14)
    print "came here 2"
    cm = api_target.get_cloudera_manager()
    try:
        cm.create_peer(settings.peer_name, settings.source_cm_url, settings.source_user, settings.source_password)
    except ApiException as e:
        if 'already exists' in str(e):
            print 'Peer Already exists'
        else:
            raise e


    return 0

if __name__ == '__main__':
    sys.exit(main())



