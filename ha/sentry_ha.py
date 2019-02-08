from cm_api.api_client import ApiResource
import requests,json,os,urllib
from cm_api.endpoints.services import ApiServiceSetupInfo
from cm_api.endpoints import roles, role_config_groups
import cm_client

CM_IP="sam-1.vpc.cloudera.com"
CDH_CLUST_NAME="cluster 1"
CM_PROTO='http'
CM_PORT='7180'
new_sentry_host = "sam-2.vpc.cloudera.com"
cluster_name = 'cluster_1'


def get_sentry_role_name():
    cluster = api.get_cluster(cluster_name)
    services =  cluster.get_all_services()
    for service in services:
        if service.type == "SENTRY":
            roles = service.get_all_roles()
            return roles[1].name


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
    print url
    api = ApiResource(CM_IP, CM_PORT, 'admin', 'admin', version=15)
    new_sentry_host_id = get_host_id(new_sentry_host)
    print new_sentry_host_id
    zk_service_name = get_service_name('ZOOKEEPER', api, 'cluster_1')
    print zk_service_name
    sentry_role_name = get_sentry_role_name()
    print sentry_role_name
    arguments={
        "newSentryHostId": new_sentry_host_id,
        "newSentryRoleName": sentry_role_name,
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
    print enable.content
    print enable.status_code




