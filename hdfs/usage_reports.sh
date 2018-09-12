#!/usr/bin/env bash
curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/ \
hdfs1/reports/hdfsUsageReport?nameservice=nameservice1&aggregation=daily'