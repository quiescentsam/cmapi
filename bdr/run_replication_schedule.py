#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *

hdfs = api_root.get_cluster(TARGET_CLUSTER_NAME).get_service(TARGET_HDFS_NAME)

cmd = hdfs.trigger_replication_schedule(schedule.id)



cmd = cmd.wait()
result = hdfs.get_replication_schedule(schedule.id).history[0].hdfsResult
