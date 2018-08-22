#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *
from ReplicationResult import ApiHdfsReplicationResult
import argparse,sys

def parse_args():
    """
    Parses host and cluster information from the given command line arguments.
    @rtype:  namespace
    @return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Adding Source cluster as 'peer' in Destination Cloudera Manager ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--server', metavar='HOST', type=str, help="The Cloudera Manager host")
    parser.add_argument('-p', '--port', metavar='port', type=int, default=7180, help="Cloudera Manager's port.")
    parser.add_argument('-u', '--username', metavar='USERNAME', type=str, default='admin',
                        help="The username to log into Cloudera Manager with.")
    parser.add_argument('-pwd', '--password', metavar='PASSWORD', type=str, default='admin',
                        help="The password to log into Cloudera Manager with.")
    parser.add_argument('--use-tls', action='store_true', help="Whether to use TLS to connect to Cloudera Manager.")
    parser.add_argument('-id', '--schedule-id', metavar='Schedule ID')
    parser.add_argument('-tc','--target-cluster-name', metavar='Destination Cluster Name')
    return parser.parse_args()


def print_usage_message():
    print ("usage: run_replication_schedule.py [-h] [-s HOST] [-p port] [-u USERNAME] \
          [-pwd PASSWORD] [--use-tls] \
          [-id Schedule ID] \
          [-tc Destination Cluster Name]")


def get_service_name(SERVICE_TYPE, cluster_api, CLUSTER_NAME):
    """
    Inputs: Common name of the Service,cluster APiResource and cluster name
    :return: Service name , returns "None" if service is not present
    """
    cluster = cluster_api.get_cluster(CLUSTER_NAME)
    services = cluster.get_all_services()
    for service_name in services:
        if SERVICE_TYPE in service_name.name:
            return service_name.name


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

    api = ApiResource(settings.server, settings.port, settings.username,settings.password, settings.use_tls, 14)
    TARGET_HDFS_NAME = get_service_name('HDFS',api, settings.target_cluster_name)
    hdfs = api.get_cluster(settings.target_cluster_name).get_service(TARGET_HDFS_NAME)
    # schs = hdfs.get_replication_schedules()
    # print schs
    cmd = hdfs.trigger_replication_schedule(settings.schedule_id)
    cmd = cmd.wait()
    result = hdfs.get_replication_schedule(settings.schedule_id).history[0].hdfsResult
    print result

    return 0

if __name__ == '__main__':
    sys.exit(main())