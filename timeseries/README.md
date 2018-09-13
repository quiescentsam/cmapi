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
