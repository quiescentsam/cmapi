# Generate HDFS Disk Usage reports using the Cloudera Manager API

## Notes:
1. The API supports aggregation by month, day and hour thus the offerings in the Web UI "Current" and "Historical" combined.
2. When using NameNode HA you must include the "NameService" parameter


**see the list of service to get HDFS service name**

```
curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services'
```
**Generate HDFS usage report and output to csv**

```
curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily' -H "Accept: text/csv" -o hdfsUsageReport_default.csv
```
```shell
By Now and Daily 
$ curl -v -k -X GET -u admin:admin 'http://cm.example.com:7180/api/v5/clusters/Cluster%201/services/hdfs/reports/hdfsUsageReport' -H "Accept: text/csv" -o hdfsUsageReport_default.csv
By DateRange and Week:
$ curl -v -k -X GET -u admin:admin 'http://cm.example.com:7180/api/v5/clusters/Cluster%201/services/hdfs/reports/hdfsUsageReport?from=2014-08-01&to=2014-08-21&aggregation=weekly' -H "Accept: text/csv" -o hdfsUsageReport_weekly.csv
By DateRange and Hour:
$ curl -v -k -X GET -u admin:admin 'http://cm.example.com:7180/api/v5/clusters/Cluster%201/services/hdfs/reports/hdfsUsageReport?from=2014-08-01&to=2014-08-21&aggregation=hourly' -H "Accept: text/csv" -o hdfsUsageReport_hourly.csv

```


Sample report

```shell
bash-3.2$ cat hdfsUsageReport_default.csv
date,user,size,rawSize,numFiles
"2018-09-12T14:53:56.000Z",oozie,584314888,1752944664,723
"2018-09-12T14:53:56.000Z",hive,1355599,4066797,73
"2018-09-12T14:53:56.000Z",hue,0,0,405
"2018-09-12T14:53:56.000Z",hdfs,0,0,12
"2018-09-12T14:53:56.000Z",solr,0,0,1
"2018-09-12T14:53:56.000Z",spark,0,0,2
"2018-09-12T14:53:56.000Z",sqoop2,0,0,1
"2018-09-12T14:53:56.000Z",mapred,8,24,14
"2018-09-12T14:53:56.000Z",impala,0,0,1
"2018-09-12T14:53:56.000Z",accumulo,4293,12879,30
"2018-09-12T14:53:56.000Z",hbase,6622,19866,55
"2018-09-12T14:53:56.000Z",systest,0,0,3
"2018-09-12T14:53:56.000Z",admin,414157,1242471,9
```

** does not work **
```
# Log in to the server.  This only needs to be done once.
wget --save-cookies cookies.txt \
     --keep-session-cookies \
     --post-data 'user=foo&password=bar' \
     --delete-after \
     http://server.com/auth.php

# Now grab the page or pages we care about.
wget --load-cookies cookies.txt \
     http://server.com/interesting/article.php
     
     
     export SESSION_ID=$(curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d "{\"username\": \"admin\", \"password\": \"admin\"}" http://${HOSTPORT}/api/v7/login 2>/dev/null | grep JSESSIONID | cut -d'=' -f2)
     
     # Get Cloudera Manager hostname and port.
     export CM_HOST=$(curl -i -X GET --cookie "JSESSIONID=${SESSION_ID}" "http://${HOSTPORT}/api/v7/environments/${ENVIRONMENT_NAME}/deployments/${DEPLOYMENT_NAME}" 2>/dev/null | grep "hostname" | cut -d':' -f2 | cut -d'"' -f 2 | awk "{if (NR==1) print}")
     
     # Log out from Cloudera Director and close session.
     curl -i  -H "Accept: application/json" -H "Content-Type: application/json" -X POST --cookie "JSESSIONID=${SESSION_ID}" -d "{}" http://${HOSTPORT}/api/v7/logout 2>/dev/null >dev/null

     
     
     
     
wget --save-cookies cookies.txt \
     --keep-session-cookies \
     --post-data 'user=admin&password=admin' \
     --delete-after \
     http://nightly512-1.vpc.cloudera.com:7180/cmf/login/j_spring_security_check

wget --load-cookies cookies.txt \
     -O DirectoryReport.csv http://nightly512-1.vpc.cloudera.com:7180/cmf/services/4/nameservices/ns1/reports/currentDiskUsage?groupBy=DIRECTORY&format=CSV
```




**1)  See currently watched Dir**  
```
curl -v -k -X GET -u admin:admin  http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/watcheddir
```
**2)  Add directory to watched Dir**
```
curl -v -X POST -u admin:admin -H 'Content-Type:application/json' -d '{
     "path": "/solr",
     "path": "/hbase"
}' 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/watcheddir'
```
**3) Remove directory from Watched list**
```
curl -v -X DELETE -u admin:admin -H 'Content-Type:application/json' 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/watcheddir/%2Fhbase'

```
