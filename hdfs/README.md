

curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services'



curl -v -k -X GET -u guest:guest 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily'


**Generate HDFS usage report and output to csv**

```
curl -v -k -X GET -u admin:admin 'http://nightly512-1.vpc.cloudera.com:7180/api/v14/clusters/Cluster%201/services/HDFS-1/reports/hdfsUsageReport?nameservice=ns1&aggregation=daily' -H "Accept: text/csv" -o hdfsUsageReport_default.csv
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
