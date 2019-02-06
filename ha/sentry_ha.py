from cm_api.api_client import ApiResource
import requests
from cm_api.endpoints.services import 

cm_host = "sam-1.vpc.cloudera.com"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'

api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=15)
cluster = api.get_cluster()



args = dict(
    newSentryHostId = new_sentry_host_id,
    newSentryRoleName =  new_sentry_role_name,
    zkServiceName = zk_service_name,
    rrcArgs = {
        "slaveBatchSize" : 12345,
        "sleepSeconds" : 12345,
        "slaveFailCountThreshold" : 12345
    })


enable = requests.post("http://sam-1.vpc.cloudera.com:7180/clusters/cluster_1/services/sentry/commands/enableSentryHa", args)

def enable_sentry_ha(self, new_sentry_host_id, new_sentry_role_name, zk_service_name):
    args = dict(
            newSentryHostId = new_sentry_host_id,
            newSentryRoleName =  new_sentry_role_name,
            zkServiceName = zk_service_name,
            rrcArgs = {
                "slaveBatchSize" : 12345,
                "sleepSeconds" : 12345,
                "slaveFailCountThreshold" : 12345
            }
    )
    return self._cmd('enableSentryHa', data=args)

# def enable_rm_ha(self, new_rm_host_id, zk_service_name=None):
#     """
#     Enable high availability for a YARN ResourceManager.
#     @param new_rm_host_id: id of the host where the second ResourceManager
#                            will be added.
#     @param zk_service_name: Name of the ZooKeeper service to use for auto-failover.
#            If YARN service depends on a ZooKeeper service then that ZooKeeper
#            service will be used for auto-failover and in that case this parameter
#            can be omitted.
#     @return: Reference to the submitted command.
#     @since: API v6
#     """
#     args = dict(
#         newRmHostId = new_rm_host_id,
#         zkServiceName = zk_service_name
#     )
#     return self._cmd('enableRmHa', data=args)

