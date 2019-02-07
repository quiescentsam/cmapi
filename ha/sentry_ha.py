from cm_api.api_client import ApiResource
import requests,json
from cm_api.endpoints.services import ApiServiceSetupInfo
from cm_api.endpoints import roles, role_config_groups

cm_host = "bluedata-gsk-1.vpc.cloudera.com"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'
new_sentry_host = "bluedata-gsk-5.vpc.cloudera.com"

api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=15)
hosts = api.get_all_hosts()


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

def get_role_name():
    role_name=requests.get('http://bluedata-gsk-1.vpc.cloudera.com:7180/api/v19/clusters/cluster_1/services/sentry/roles')
    print role_name
    return role_name

if __name__ == '__main__':
    new_sentry_host_id = get_host_id(new_sentry_host)
    print new_sentry_host_id
    zk_service_name = get_service_name('ZOOKEEPER', api, 'cluster_1')
    print zk_service_name
    arguments={
        "newSentryHostId": new_sentry_host_id,
        "newSentryRoleName": "sentry-SENTRY_SERVER-5e590a9a495e2b4b7cca67babca370d0",
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

    enable = requests.post("http://bluedata-gsk-1.vpc.cloudera.com:7180/api/v19/clusters/cluster_1/services/sentry/commands/enableSentryHa", auth=('admin', 'admin'), data=json.dumps(arguments), headers=headers )
    print enable

    role_name=requests.get('http://bluedata-gsk-1.vpc.cloudera.com:7180/api/v19/clusters/cluster_1/services/sentry/roles', auth=('admin', 'admin'))
    print role_name.