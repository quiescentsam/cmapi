#!/usr/bin/env python


## *******************************************************************************************
##  run_replication_schedule.py
##
##  Executes the Replication Schedule
##
##  Usage: python run_replication_schedule.py -s <CM hostname> -id <schdule id> --target-cluster-name <target cluster name>
##
##   python run_replication_schedule.py [-h] [-s HOST] [-p port] [-u USERNAME]
##    [-pwd PASSWORD] [--use-tls]
##    [-id Schedule ID]
##    [-tc Destination Cluster Name]"
##
##    Set queryRunningSeconds to the threshold considered "too long"
##    for an Impala query to run, so that queries that have been running
##    longer than that will be identifed as queries to be killed
##
##    The second argument "KILL" is optional
##    Without this argument, no queries will actually be killed, instead a list
##    of queries that are identified as running too long will just be printed to the console
##    If the argument "KILL" is provided a cancel command will be issues for each selcted query
##
##    CM versions <= 5.4 require Full Administrator role to cancel Impala queries
##
##    Set the CM URL, Cluster Name, login and password in the settings below
##
##    This script assumes there is only a single Impala service per cluster
##
## *******************************************************************************************

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
    parser.add_argument('-id', '--schedule-id', metavar='Schedule ID', type=int)
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
    cmd = hdfs.trigger_replication_schedule(settings.schedule_id)
    cmd.wait()
    result = hdfs.get_replication_schedule(settings.schedule_id).history[0]
    hdfsresult = hdfs.get_replication_schedule(settings.schedule_id).history[0].hdfsResult
    if result.success == False:
        print "######  Replication job failed  #####"
        print "Yarn Job ID :" + str(hdfsresult.jobId)
        print "Job Details URL:" + str(hdfsresult.jobDetailsUri)
        print "Setup Error:" + str(hdfsresult.setupError)
    else:
        print "######  Replication job succeeded  #####"
        print "Yarn Job ID :" + str(hdfsresult.jobId)
        print "Job Details URL:" + str(hdfsresult.jobDetailsUri)
        print "numFilesCopied:" + str(hdfsresult.numFilesCopied)
        print "numBytesCopied:" + str(hdfsresult.numBytesCopied)
        print "numFilesSkipped:" + str(hdfsresult.numFilesSkipped)
        print "numBytesSkipped:" + str(hdfsresult.numBytesSkipped)


    return 0

if __name__ == '__main__':
    sys.exit(main())