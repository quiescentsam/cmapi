from cm_api.api_client import ApiResource
import requests,json,urllib

CM_IP="sam-1.vpc.cloudera.com"
CDH_CLUST_NAME="cluster 1"
CM_PROTO='http'
CM_PORT='7180'
NEW_SENTRY_HOST = "sam-3.vpc.cloudera.com"


def get_host_id(hostname):
    hosts = api.get_all_hosts()
    for host in hosts:
        if host.hostname == hostname:
            return host.hostId


def get_service_name(service_type, api, cluster_name):
    """
    Inputs: Common name of the Service,cluster APiResource and cluster name
    :return: Service name , returns "None" if service is not present
    """
    cluster = api.get_cluster(cluster_name)
    services = cluster.get_all_services()
    for service_name in services:
        if service_type in service_name.type:
            return service_name.name

if __name__ == '__main__':
    CDH_CLUST_NAME = urllib.quote(CDH_CLUST_NAME)
    url = CM_PROTO + '://' + CM_IP + ':' + CM_PORT + '/api/v19/clusters/' + CDH_CLUST_NAME + '/services/sentry/commands/enableSentryHa'
    api = ApiResource(CM_IP, CM_PORT, 'admin', 'admin', version=15)
    new_sentry_host_id = get_host_id(NEW_SENTRY_HOST)
    zk_service_name = get_service_name('ZOOKEEPER', api, 'cluster_1')
    arguments={
        "newSentryHostId": new_sentry_host_id,
        "newSentryRoleName": "secondsentryserver",
        "zkServiceName": zk_service_name,
        "rrcArgs": {
            "slaveBatchSize": 10,
            "sleepSeconds": 10,
            "slaveFailCountThreshold": 10
        }
    }
    headers = {
        'Content-Type': 'application/json',
    }

    enable = requests.post(url , auth=('admin', 'admin'), data=json.dumps(arguments), headers=headers )
    result = enable.content
    response = json.loads(result)
    print enable.status_code
    print response["resultMessage"]



