https://cloudera.app.box.com/file/75000334202 (CM API for partners)
https://cloudera.app.box.com/file/124546077676 (Navigator Lineage)
https://wiki.cloudera.com/display/~svenkataramanasam/CM+API+examples
https://wiki.cloudera.com/display/PRODUCT/CM+API+integration+with+other+tools

https://wiki.cloudera.com/display/COPS/CM+API+curl+usage+examples

https://archive.cloudera.com/cm6/6.1.0/generic/jar/cm_api/apidocs/index.html

https://cloudera.github.io/cm_api/docs/python-client-swagger/

https://github.com/cloudera/cm_api




## escape characters

%2F - for slashes  
%20 - for spaces



## CM API SAMPLES

```bash
curl -su spgdevadmin:'XYZ' -X GET 'https://dal01d-gen-cdh-cmn001.dalab.syniverse.com:7183/api/v13/clusters/Dallas%20Lab%20(Corp)%20Cluster/services/impala/impalaQueries?filter=(query_duration>1ms)&from=2018-06-20&to=2018-06-20T23:59:59'

```

`-u` is for username and password authentication

curl -su admin:admin http://nightly514-1.gce.cloudera.com:7180/api/v19/clusters/Cluster%201/export  > cluster.json


http://cloudera.github.io/cm_api/apidocs/v19/path__clusters_-clusterName-_services_-serviceName-_replications_-scheduleId-_run.html


## to get cloudera manager config from the clusters
```
wget --user --password admin -O cminfo.json http://host:7180/api/v19/cm/deployment?view=export_redacted --no-check-certificate
```

## to get the CDH config from the clusters
```
wget --user --password admin -O cluster_info.json http://nightly514-1.gce.cloudera.com:7180/api/v19/clusters/Cluster%201/export --no-check-certificate
```


3.Update scmdb.json

wget --user --password admin -O cmdb.json http://host:7180/api/v19/cm/scmDbInfo?view=export_redacted
--no-check-certificate


---
## Scripts

1. CM dump config [example](scripts/cm-dump-config.md)



Java Example:

https://github.com/namrata01/cloudera-manager-automation

Genreric
https://github.com/jameyhanson/CM_API
