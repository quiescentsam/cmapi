#!/usr/bin/env bash



curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services'



curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily'