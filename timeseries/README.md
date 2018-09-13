Generate Historical TimeSeries reports (e.g. Application, Impala) using the Cloudera Manager API

Step 1 : Generate Base JSON Queries:
1. Navigate to Reports in Cloudera Manager
2. Click Historical report (e.g. Applications, Impala Queries)
3. Modify StartDate, EndDate and ReportPeriod as necessary
4. Choose a reporting section (e.g. Graph, Table)
5. Hover over top right area to illuminate drop down button
6. Click drop down button
7. Click "Export JSON" button
8. Capture url from browser
Historical Applications (Daily):
http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(apps_ingested_rate)+WHERE+serviceName%3D%22yarn%22+AND+CATEGORY%3DSERVICE&contentType=application%2Fjson&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true
Historical Queries (Daily):
http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(queries_ingested_rate)+WHERE+serviceName%3D%22impala%22+AND+CATEGORY%3DSERVICE&contentType=application%2Fjson&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true


Step 2 : Configure Output Type:
1. If JSON is the desired output leave as is
2. If CSV is the desired output modify "contentType" (from: contentType=application%2Fjson to: contentType=text%2Fcsv)

Historical Applications (Daily) CSV:
http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(apps_ingested_rate)+WHERE+serviceName%3D%22yarn%22+AND+CATEGORY%3DSERVICE&contentType=text%2Fcsv&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true
Historical Queries (Daily) CSV:
http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(queries_ingested_rate)+WHERE+serviceName%3D%22impala%22+AND+CATEGORY%3DSERVICE&contentType=text%2Fcsv&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true


Step 3 : Create Curl Command:
1. Create command template (e.g. curl -v -k -X GET -u admin:admin '<query>' -o <filename>)
2. Paste query into command template
3. Execute commands  

Historical Applications (Daily) CSV Query:
$ curl -v -k -X GET -u admin:admin 'http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(apps_ingested_rate)+WHERE+serviceName%3D%22yarn%22+AND+CATEGORY%3DSERVICE&contentType=text%2Fcsv&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true' -o applicationsReport_daily.csv

Historical Queries (Daily) CSV:
$ curl -v -k -X GET -u admin:admin 'http://cm.example.com:7180/api/v6/timeseries?query=SELECT+integral(queries_ingested_rate)+WHERE+serviceName%3D%22impala%22+AND+CATEGORY%3DSERVICE&contentType=text%2Fcsv&from=2014-08-01T00%3A00%3A00.000Z&to=2014-08-26T23%3A59%3A59.999Z&desiredRollup=DAILY&mustUseDesiredRollup=true' -o queriesReport.csv

Sample Column Output:
$ cat applicationsReport_daily.csv
entityName,metricName,timestamp,value
$ cat queriesReport.csv
entityName,metricName,timestamp,value



PYTHON SCRIPT


https://github.com/cloudera/cm_api/blob/master/python/examples/timeseries.py


list of queries:
DFS USED - SELECT dfs_capacity_used/(1024*1024)

EXECUTION examples

(python27) bash-3.2$ python timeseries.py "SELECT dfs_capacity_used/(1024*1024)"
<ApiTimeSeriesResponse>
  query: SELECT dfs_capacity_used/(1024*1024)
  timeSeries:
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: NameNode (nightly512-1.vpc.cloudera.com)
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'ROLE', u'roleType': u'NAMENODE', u'serviceType': u'HDFS', u'hostname': u'nightly512-1.vpc.cloudera.com', u'rackId': u'/default', u'version': u'CDH 5.12.3', u'clusterName': u'Cluster 1', u'entityName': u'HDFS-1-NAMENODE-1e9aa0b0980c2af85b415ac36c220dea', u'clusterDisplayName': u'Cluster 1', u'hostId': u'041904d6-43eb-4584-9ac2-cd6b4a9a54ed', u'roleConfigGroup': u'NameNode Default Group', u'active': u'true', u'roleName': u'HDFS-1-NAMENODE-1e9aa0b0980c2af85b415ac36c220dea', u'serviceName': u'HDFS-1'}
    data:
      timestamp: 2018-09-13 15:45:34 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:46:34 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:47:34 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:48:34 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:49:34 value: 1696.96875 type: CALCULATED
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: NameNode (nightly512-2.vpc.cloudera.com)
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'ROLE', u'roleType': u'NAMENODE', u'serviceType': u'HDFS', u'hostname': u'nightly512-2.vpc.cloudera.com', u'rackId': u'/default', u'version': u'CDH 5.12.3', u'clusterName': u'Cluster 1', u'entityName': u'HDFS-1-NAMENODE-0e525f97c4c3307aba0da60e6f643656', u'clusterDisplayName': u'Cluster 1', u'hostId': u'627b4dde-7b68-46a5-a15b-a43029dae6be', u'roleConfigGroup': u'NameNode Default Group', u'active': u'true', u'roleName': u'HDFS-1-NAMENODE-0e525f97c4c3307aba0da60e6f643656', u'serviceName': u'HDFS-1'}
    data:
      timestamp: 2018-09-13 15:45:30 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:46:30 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:47:30 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:48:30 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:49:30 value: 1696.96875 type: CALCULATED
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: HDFS-1
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'SERVICE', u'serviceType': u'HDFS', u'clusterName': u'Cluster 1', u'serviceDisplayName': u'HDFS-1', u'clusterDisplayName': u'Cluster 1', u'version': u'CDH 5.12.3', u'active': u'true', u'serviceName': u'HDFS-1:ns1', u'entityName': u'HDFS-1:ns1'}
    data:
      timestamp: 2018-09-13 15:45:55.826000 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:46:55.833000 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:47:55.834000 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:48:55.838000 value: 1696.96875 type: CALCULATED
      timestamp: 2018-09-13 15:49:55.835000 value: 1696.96875 type: CALCULATED
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: DataNode (nightly512-4.vpc.cloudera.com)
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'ROLE', u'roleType': u'DATANODE', u'serviceType': u'HDFS', u'hostname': u'nightly512-4.vpc.cloudera.com', u'rackId': u'/default', u'version': u'CDH 5.12.3', u'clusterName': u'Cluster 1', u'entityName': u'HDFS-1-DATANODE-533d17f28b18ca08d4fb7b834841196d', u'clusterDisplayName': u'Cluster 1', u'hostId': u'a9f45ef2-1772-452c-b567-c96f32890f57', u'roleConfigGroup': u'DataNode Default Group', u'active': u'true', u'roleName': u'HDFS-1-DATANODE-533d17f28b18ca08d4fb7b834841196d', u'serviceName': u'HDFS-1'}
    data:
      timestamp: 2018-09-13 15:45:55.826000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:46:55.833000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:47:55.834000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:48:55.838000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:49:55.835000 value: 565.65625 type: CALCULATED
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: DataNode (nightly512-3.vpc.cloudera.com)
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'ROLE', u'roleType': u'DATANODE', u'serviceType': u'HDFS', u'hostname': u'nightly512-3.vpc.cloudera.com', u'rackId': u'/default', u'version': u'CDH 5.12.3', u'clusterName': u'Cluster 1', u'entityName': u'HDFS-1-DATANODE-4fd629377c3cce1503471e3e5e3aa2a1', u'clusterDisplayName': u'Cluster 1', u'hostId': u'b4c80cfc-0f6b-459d-8342-b3215adcf3fd', u'roleConfigGroup': u'DataNode Default Group', u'active': u'true', u'roleName': u'HDFS-1-DATANODE-4fd629377c3cce1503471e3e5e3aa2a1', u'serviceName': u'HDFS-1'}
    data:
      timestamp: 2018-09-13 15:45:55.826000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:46:55.833000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:47:55.834000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:48:55.838000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:49:55.835000 value: 565.65625 type: CALCULATED
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: HDFS-1
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'SERVICE', u'serviceType': u'HDFS', u'clusterName': u'Cluster 1', u'serviceDisplayName': u'HDFS-1', u'clusterDisplayName': u'Cluster 1', u'version': u'CDH 5.12.3', u'active': u'true', u'serviceName': u'HDFS-1', u'entityName': u'HDFS-1'}
    data:
    metadata:
      metricName: dfs_capacity_used/(1024*1024)
      entityName: DataNode (nightly512-2.vpc.cloudera.com)
      startTime: 2018-09-13 15:44:58.465000
      endTime: 2018-09-13 15:49:58.465000
      unitNumerators: [u'bytes']
      attributes: {u'category': u'ROLE', u'roleType': u'DATANODE', u'serviceType': u'HDFS', u'hostname': u'nightly512-2.vpc.cloudera.com', u'rackId': u'/default', u'version': u'CDH 5.12.3', u'clusterName': u'Cluster 1', u'entityName': u'HDFS-1-DATANODE-0e525f97c4c3307aba0da60e6f643656', u'clusterDisplayName': u'Cluster 1', u'hostId': u'627b4dde-7b68-46a5-a15b-a43029dae6be', u'roleConfigGroup': u'DataNode Default Group', u'active': u'true', u'roleName': u'HDFS-1-DATANODE-0e525f97c4c3307aba0da60e6f643656', u'serviceName': u'HDFS-1'}
    data:
      timestamp: 2018-09-13 15:45:55.826000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:46:55.833000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:47:55.834000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:48:55.838000 value: 565.65625 type: CALCULATED
      timestamp: 2018-09-13 15:49:55.835000 value: 565.65625 type: CALCULATED
(python27) bash-3.2$
