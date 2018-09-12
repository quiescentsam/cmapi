#!/usr/bin/env bash



curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services'



curl -v -k -X GET -u guest:guest 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily'



curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily' -H "Accept: text/csv" -o hdfsUsageReport_default.csv



1) See currently watched DIR
curl -v -k -X GET -u admin:admin  http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/watcheddir

1)
Add directory to watched Dir

curl -v -X POST -u admin:admin -H 'Content-Type:application/json' -d '{
     "watchedDir": "/solr"
}' 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/watcheddir'




curl --cookie-jar ./mycookies.txt --data "j_username=admin&j_password=admin" http://nightly512-1.vpc.cloudera.com:7180/cmf/login/j_spring_security_check


(2)
Add /solr path as a watched dir


curl --cookie ./mycookies.txt --data "path=%2Fsolr" http://nightly512-1.vpc.cloudera.com:7180/cmf/services/HDFS-1/watcheddir
curl -v -k -X GET -u admin:admin http://nightly512-1.vpc.cloudera.com:7180/cmf/services/HDFS-1/watcheddir
curl -v -k -X POST -u admin:admin --data "path=%2Fsolr" http://nightly512-1.vpc.cloudera.com:7180/cmf/services/HDFS-1/watcheddir
(3)
Remove /solr path as a watched dir


curl --cookie ./mycookies.txt --data "path=%2Fsolr" http://nightly512-1.vpc.cloudera.com:7180/cmf/services/3/watcheddir/remove