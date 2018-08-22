#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *
from ReplicationResult import ApiHdfsReplicationResult

PEER_NAME='peer1'
SOURCE_CLUSTER_NAME='sameer-testspot'
SOURCE_HDFS_NAME='CD-HDFS-VHPVExTo'
TARGET_CLUSTER_NAME='sameer-testspot-dest'
TARGET_HDFS_NAME='CD-HDFS-KukHKtDK'
TARGET_YARN_SERVICE='YARN-1CD-YARN-rnMjblqZ'
TARGET_CM_HOST="18.205.59.216"


api_root = ApiResource(TARGET_CM_HOST, username="admin", password="admin")
hdfs = api_root.get_cluster(TARGET_CLUSTER_NAME).get_service(TARGET_HDFS_NAME)


schs = hdfs.get_replication_schedules()
print schs
# cmd = hdfs.trigger_replication_schedule(6)
# cmd = cmd.wait()
# result = hdfs.get_replication_schedule(6).history[0].hdfsResult
result = hdfs.get_replication_schedules()
