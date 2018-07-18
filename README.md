#CM API SAMPLES

```bash
curl -su spgdevadmin:'XYZ' -X GET 'https://dal01d-gen-cdh-cmn001.dalab.syniverse.com:7183/api/v13/clusters/Dallas%20Lab%20(Corp)%20Cluster/services/impala/impalaQueries?filter=(query_duration>1ms)&from=2018-06-20&to=2018-06-20T23:59:59'

```

`-u` is for username and password authentication

curl -su admin:admin http://nightly514-1.gce.cloudera.com:7180/api/v19/clusters/Cluster%201/export  > cluster.json


http://cloudera.github.io/cm_api/apidocs/v19/path__clusters_-clusterName-_services_-serviceName-_replications_-scheduleId-_run.html

---
## Scripts

1. CM dump config 