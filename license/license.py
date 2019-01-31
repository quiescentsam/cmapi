from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

cm_host = "nightly515-1.vpc.cloudera.com"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'
license_file = '/Users/ssiddiqui/Desktop/SAMEER2.0/WORK/CODE/cloud/sameer_ahmad_siddiqui_cloudera_enterprise_license.txt'


api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=7)
cm = ClouderaManager(api)
license = open(license_file, 'r').read()
cm.update_license(license)
