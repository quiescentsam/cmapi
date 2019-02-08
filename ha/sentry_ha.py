from cm_api.api_client import ApiResource
import requests,json,os,urllib
from cm_api.endpoints.services import ApiServiceSetupInfo
from cm_api.endpoints import roles, role_config_groups
import cm_client

CM_IP="sam-1.vpc.cloudera.com"
CDH_CLUST_NAME="cluster 1"
CM_PROTO='http'
CM_PORT='7180'
new_sentry_host = "sam-3.vpc.cloudera.com"
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
        "newSentryRoleName": "rolesentry",
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
    result= enable.content
    print json.loads(result)
    print enable.status_code
    print 



# /Users/ssiddiqui/.conda/envs/cmapi/bin/python /Users/ssiddiqui/Desktop/SAMEER2.0/WORK/CODE/cmapi/ha/sentry_ha.py
# http://sam-1.vpc.cloudera.com:7180/api/v19/clusters/cluster%201/services/sentry/commands/enableSentryHa
# db77c41f-f10e-4941-bc14-7562fc58056b
# zookeeper
# sentry-SENTRY_SERVER-ebbe4edca874a0e083507577a9d20714
# {u'active': True, u'serviceRef': {u'clusterName': u'cluster_1', u'serviceName': u'sentry'}, u'id': 424, u'startTime': u'2019-02-08T17:45:14.125Z', u'name': u'EnableSentryHA'}
# 200


