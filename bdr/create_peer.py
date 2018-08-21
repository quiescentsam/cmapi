#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *

TARGET_CM_HOST = "<destination_cluster>"
SOURCE_CM_URL = "<source_cluster>:7180/"

api_root = ApiResource(TARGET_CM_HOST, username="<username>", password="<password>")
cm = api_root.get_cloudera_manager()
cm.create_peer("peer1", SOURCE_CM_URL, '<username>', '<password>')