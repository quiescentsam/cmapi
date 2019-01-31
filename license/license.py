from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

cm_host = "nightly515-1.vpc.cloudera.com"
cm_port = 7180
cm_username = 'admin'
cm_password = 'admin'


api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=7)
cm = ClouderaManager(api)
linestring = open('/Users/ssiddiqui/Desktop/SAMEER2.0/WORK/CODE/cloud/sameer_ahmad_siddiqui_cloudera_enterprise_license.txt', 'r').read()
license = cm.get_license()
cm.update_license(linestring)





# update = cm.update_license("""-----BEGIN PGP SIGNED MESSAGE-----
# Hash: SHA256
#
# {
#     "features" : [ ],
#     "name" : "Sameer_Ahmad_Siddiqui",
#     "uuid" : "c09b32e4-ce0a-419d-8080-c24350b11a02",
#     "version" : 1,
#     "expirationDate" : "2019-07-16"
# }
# -----BEGIN PGP SIGNATURE-----
# Version: BCPG v1.46
#
# iQIcBAEBCAAGBQJbTg+6AAoJECXwRXLmH8tlMfYQAIhzhCrvo4aQJ/xLPgkJT7M+
# FUJiGVaGqdDXPxeD0D5PzYV15hxBHuXvlG7QIHfdEphZqpOdvBfpLGVlBjWJEsev
# lFzfDXSZ/SOVHXFUDp0K2RMvQsh+fIt2PwcBClkEzQE5C+ebBnGowXG3Gee+0lvK
# Alp6S3kwSJkQQfmvv8WvbwUtFka2ScLDGQqs3Q+wQqbMvgWTPYuIoKKs5Wr9aH/l
# QzrMa/XfSzq0aDjBEM2y8f4kW/qCEDaPZjLn35aDmwkTzWpmxxkZROAF3Sv3fddg
# /LT3AgdrRqcdcO26GM7D882hqp8EA8s3Z12e5CrZyKr+WKPUHeIxP4+QxAHv13r9
# UBCn0smr3N0kS4U5HtufWgePSbMMETRizheO1GMgye2t1O6apyrjq8c2GKPYRAuI
# eKo0CFWegN/xVjLf2yHhr2dmGNkHNET6NuABLiLnrw3PkuN33ismhkIOjFfJ8Bql
# AMnEfBJJLFGcTc7KcAWNetM9qUMdxJqf9DhSoRzjyjN7YmzP94OV2C8Ii8ZQ5eYH
# 4eMxXvqQJ7xRQ6zPfjS6nycrVtonIOyilnu2NQtTf27P/YCiZI03D5HnG7IJQsRi
# 64Nw10XjmIJEsbcSqrTOL5exrnBvoP5ovH0EmMXglmc84nsU2G6kUmxlXxRdJIs6
# vClUuf2gJ0HvaP2b1JAs
# =1sEX
#   -----END PGP SIGNATURE-----""")

