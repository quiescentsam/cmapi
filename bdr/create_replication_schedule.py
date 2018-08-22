#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *

# def get_service_name():
#     """
#     Take the cluster APiResource and get SERVICE name
#     :return:
#     """
#     api_target = ApiResource(TARGET_CM_HOST, username="admin", password="admin")
#     cluster = api_target.get_cluster(TARGET_CLUSTER_NAME)
#     services = cluster.get_services()
#     print services

TARGET_CM_HOST="18.205.59.216"
TARGET_CLUSTER_NAME='sameer-testspot-dest'
api_target = ApiResource(TARGET_CM_HOST, username="admin", password="admin")
cluster = api_target.get_cluster(TARGET_CLUSTER_NAME)
services = cluster.get_all_services()
print services[1].name
for a in services.name:
    print a
print type(services)

# PEER_NAME='peer1'
# SOURCE_CLUSTER_NAME='sameer-testspot'
# SOURCE_HDFS_NAME='CD-HDFS-VHPVExTo'
# TARGET_CLUSTER_NAME='sameer-testspot-dest'
# TARGET_HDFS_NAME='CD-HDFS-KukHKtDK'
# TARGET_YARN_SERVICE='CD-YARN-rnMjblqZ'
# TARGET_CM_HOST="18.205.59.216"
#
# api_root = ApiResource(TARGET_CM_HOST, username="admin", password="admin")
# hdfs = api_root.get_cluster(TARGET_CLUSTER_NAME).get_service(TARGET_HDFS_NAME)
#
# hdfs_args = ApiHdfsReplicationArguments(None)
# hdfs_args.sourceService = ApiServiceRef(None,
#                                         peerName=PEER_NAME,
#                                         clusterName=SOURCE_CLUSTER_NAME,
#                                         serviceName=SOURCE_HDFS_NAME)
# hdfs_args.sourcePath = '/'
# hdfs_args.destinationPath = '/'
# hdfs_args.mapreduceServiceName = TARGET_YARN_SERVICE
#
# # creating a schedule with daily frequency
# start = datetime.datetime.now() # The time at which the scheduled activity is triggered for the first time.
# end = start + datetime.timedelta(days=365) # The time after which the scheduled activity will no longer be triggered.
#
# schedule = hdfs.create_replication_schedule(start, end, "DAY", 1, True, hdfs_args)