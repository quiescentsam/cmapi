#BDR automation

###To Do
* add S3 connector - Done
* Update add replication schdule to accept S3 dest

##ADD Peer

```(python27) ssiddiqui-MBP15:bdr ssiddiqui$ python add_peer.py -h
usage: add_peer.py [-h] [-s HOST] [-p port] [-u USERNAME] [-pwd PASSWORD]
                   [--use-tls] [--source_cm_url Source Cloudera Manager URL]
                   [--source-user Source Cloudera Manager Username]
                   [--source-password SOURCE_CM_PWD] [--peer-name PEER_NAME]

Adding Source cluster as 'peer' in Destination Cloudera Manager

optional arguments:
  -h, --help            show this help message and exit
  -s HOST, --server HOST
                        The Cloudera Manager host (default: None)
  -p port, --port port  Cloudera Manager's port. (default: 7180)
  -u USERNAME, --username USERNAME
                        The username to log into Cloudera Manager with.
                        (default: admin)
  -pwd PASSWORD, --password PASSWORD
                        The password to log into Cloudera Manager with.
                        (default: admin)
  --use-tls             Whether to use TLS to connect to Cloudera Manager.
                        (default: False)
  --source_cm_url Source Cloudera Manager URL
                        Full CM URL of the source cluster ie.
                        https://hostname:7183/ (default: None)
  --source-user Source Cloudera Manager Username
                        The username to log into Source Cloudera Manager with.
                        (default: admin)
  --source-password SOURCE_CM_PWD
                        The password to log into Source Cloudera Manager with.
                        (default: admin)
  --peer-name PEER_NAME
                        ALias Name to be created of the Source cluster
                        (default: peer1)

```

## Create a Schedule

```
(python27) bash-3.2$ python create_replication_schedule.py -h
usage: create_replication_schedule.py [-h] [-s HOST] [-p port] [-u USERNAME]
                                      [-pwd PASSWORD] [--use-tls]
                                      [--source-server Source Cloudera Manager URL]
                                      [--source-port Source port]
                                      [--source-user Source Cloudera Manager Username]
                                      [--source-password SOURCE_CM_PWD]
                                      [--s-use-tls] [--peer-name PEER_NAME]
                                      [-sp SOURCE PATH] [-tp DESTINATION PATH]
                                      [--source-cluster-name Source Cluster Name]
                                      [--target-cluster-name Destination Cluster Name]
```

## Run replication


```
(python27) ssiddiqui-MBP15:bdr ssiddiqui$ python run_replication_schedule.py -s 18.205.59.216 -id 15 --target-cluster-name sameer-testspot-dest
######  Replication job succeeded  #####
Yarn Job ID :job_1534885437444_0010
Job Details URL:/cmf/services/3/applications/?startTime=1534971867291&endTime=1534971910853#filters=application_id=job_1534885437444_0010
numFilesCopied:0
numBytesCopied:0
numFilesSkipped:8
numBytesSkipped:1430044
```



### Issues 

We might hit below issue based on CM version
https://github.com/cloudera/cm_api/issues/31 

````
class ApiHdfsReplicationResult(BaseApiObject):
  _ATTRIBUTES = {
    'progress'            : ROAttr(),
    'counters'            : ROAttr(),
    'numBytesDryRun'      : ROAttr(),
    'numFilesDryRun'      : ROAttr(),
    'numFilesExpected'    : ROAttr(),
    'numBytesExpected'    : ROAttr(),
    'numFilesCopied'      : ROAttr(),
    'numBytesCopied'      : ROAttr(),
    'numFilesSkipped'     : ROAttr(),
    'numBytesSkipped'     : ROAttr(),
    'numFilesDeleted'     : ROAttr(),
    'numFilesCopyFailed'  : ROAttr(),
    'numBytesCopyFailed'  : ROAttr(),
    'setupError'          : ROAttr(),
    'jobId'               : ROAttr(),
    'jobDetailsUri'       : ROAttr(),
    'dryRun'              : ROAttr(),
    'snapshottedDirs'     : ROAttr(),
    'failedFiles'         : ROAttr(),
    'runAsUser'           : ROAttr(),
    'remainingTime'       : ROAttr(),
    'throughput'          : ROAttr(),
  }
```