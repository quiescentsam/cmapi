PEER_NAME='peer1'
SOURCE_CLUSTER_NAME='Cluster-src-1'
SOURCE_HDFS_NAME='HDFS-src-1'
TARGET_CLUSTER_NAME='Cluster-tgt-1'
TARGET_HDFS_NAME='HDFS-tgt-1'
TARGET_YARN_SERVICE='YARN-1'

hdfs = api_root.get_cluster(TARGET_CLUSTER_NAME).get_service(TARGET_HDFS_NAME)

hdfs_args = ApiHdfsReplicationArguments(None)
hdfs_args.sourceService = ApiServiceRef(None,
                                        peerName=PEER_NAME,
                                        clusterName=SOURCE_CLUSTER_NAME,
                                        serviceName=SOURCE_HDFS_NAME)
hdfs_args.sourcePath = '/src/path/'
hdfs_args.destinationPath = '/target/path'
hdfs_args.mapreduceServiceName = TARGET_YARN_SERVICE

# creating a schedule with daily frequency
start = datetime.datetime.now() # The time at which the scheduled activity is triggered for the first time.
end = start + datetime.timedelta(days=365) # The time after which the scheduled activity will no longer be triggered.

schedule = hdfs.create_replication_schedule(start, end, "DAY", 1, True, hdfs_args)