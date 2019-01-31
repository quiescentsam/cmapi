from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

cm_host = "host00000"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'


api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=7)
cm = ClouderaManager(api)
