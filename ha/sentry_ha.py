from cm_api.api_client import ApiResource
import requests,json,os
from cm_api.endpoints.services import ApiServiceSetupInfo
from cm_api.endpoints import roles, role_config_groups
import cm_client


def __init__(self):
    self.cm_api_url = "{}://{}:{}/api/{}"
    self.cm_protocol = "http"
    #self.cm_host = os.environ['CM_IP']
    self.cm_host = os.environ['CM_IP']
    self.cluster_name = os.environ['CDH_CLUST_NAME']
    self.hidden_configs_file = os.environ['HIDDEN_CONFIGS_FILE']
    self.jinja_file_path = jinja_file_path
    self.temp_json_file_path = None
    self.cm_port = "7180"
    self.cm_api_version = "v19"
    cm_client.configuration.username = "admin"
    cm_client.configuration.password = "admin"
    self.cm_api_url = self.cm_api_url.format(self.cm_protocol, self.cm_host, self.cm_port, self.cm_api_version)
    self.api_client = cm_client.ApiClient(self.cm_api_url)
    self.services_api_client = cm_client.ServicesResourceApi(self.api_client)
    self.cluster_api_client = cm_client.ClustersResourceApi(self.api_client)
    self.role_config_groups_client = cm_client.RoleConfigGroupsResourceApi(self.api_client)


cm_host = "bluedata-gsk-1.vpc.cloudera.com"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'
new_sentry_host = "bluedata-gsk-5.vpc.cloudera.com"

api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=15)
hosts = api.get_all_hosts()
api_client = cm_client.ApiClient('http://bluedata-gsk-1.vpc.cloudera.com:7180/api/v19')
roles = cm_client.RoleConfigGroupsResourceApi()
print roles


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


