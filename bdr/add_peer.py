#!/usr/bin/env python

import argparse
import sys

from cm_api.api_client import ApiException
from cm_api.api_client import ApiResource


def parse_args():
    """
    Parses host and cluster information from the given command line arguments.
    @rtype:  namespace
    @return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Adding Source cluster as 'peer' "
                                                 "in Destination Cloudera Manager ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--server', metavar='HOST', type=str,
                        help="The Cloudera Manager host")
    parser.add_argument('-p', '--port', metavar='port', type=int, default=7180,
                        help="Cloudera Manager's port.")
    parser.add_argument('-u', '--username', metavar='USERNAME', type=str, default='admin',
                        help="The username to log into Cloudera Manager with.")
    parser.add_argument('-pwd', '--password', metavar='PASSWORD', type=str, default='admin',
                        help="The password to log into Cloudera Manager with.")
    parser.add_argument('--use-tls', action='store_true',
                        help="Whether to use TLS to connect to Cloudera Manager.")
    parser.add_argument('--source_cm_url', metavar='Source Cloudera Manager URL', type=str,
                        help="Full CM URL of the source cluster ie. https://hostname:7183/")
    parser.add_argument("--source-user", metavar='Source Cloudera Manager Username', type=str, default='admin',
                        help="The username to log into Source Cloudera Manager with.")
    parser.add_argument("--source-password", metavar='SOURCE_CM_PWD', type=str, default='admin',
                        help="The password to log into Source Cloudera Manager with.")
    parser.add_argument("--peer-name", metavar='PEER_NAME', type=str, default='peer1',
                        help="ALias Name to be created of the Source cluster")
    return parser.parse_args()


def print_usage_message():
    print "usage: add_s3account.py [-h] [-s HOST] [-p port] [-u USERNAME] [-pwd PASSWORD] \
                                [--use-tls] [--account-name ACCOUNT_NAME] \
                                [-akey AWS_ACCESS_KEY] [-skey AWS_SECRET_KEY]"


def main():
    """
    Add peer to the cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = parse_args()
    if len(sys.argv) == 1 or len(sys.argv) > 17:
        print_usage_message()
        quit(1)

    api_target = ApiResource(settings.server, settings.port, settings.username, settings.password, settings.use_tls, 14)
    cm = api_target.get_cloudera_manager()
    try:
        cm.create_peer(settings.peer_name, settings.source_cm_url, settings.source_user, settings.source_password)
        print "Peer Successfully Added"
    except ApiException as e:
        if 'already exists' in str(e):
            print 'Peer Already exists'
        else:
            raise e

    return 0


if __name__ == '__main__':
    sys.exit(main())
