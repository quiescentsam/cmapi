#!/usr/bin/env bash
curl -v -k -X GET -u admin:pw 'https://tls.cluster.com:7183/api/v14/clusters/Cluster%201/services/ \
hdfs1/reports/hdfsUsageReport?nameservice=nameservice1&aggregation=daily'