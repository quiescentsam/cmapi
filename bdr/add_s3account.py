#!/usr/bin/env python

from cm_api.api_client import ApiResource
from cm_api.endpoints.types import *
from cm_api.api_client import ApiException
import argparse
import sys


ACCESS_KEY="abcsfsg"
SECRET_KEY="asfasdgafg"
TYPE_NAME = 'AWS_ACCESS_KEY_AUTH'
account_configs ={'aws_access_key': ACCESS_KEY,
                  'aws_secret_key': SECRET_KEY}
cm.api.create_external_account("cloudAccount1",
                               "cloudAccount1",
                               TYPE_NAME,
                               account_configs=account_configs)



def main():
    """
    Add peer to the cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = parse_args()
    if len(sys.argv) == 1 or len(sys.argv) > 17:
        print_usage_message()
        quit(1)

    api_target = ApiResource(settings.server, settings.port, settings.username,settings.password, settings.use_tls, 14)
    ACCESS_KEY="abcsfsg"
    SECRET_KEY="asfasdgafg"
    TYPE_NAME = 'AWS_ACCESS_KEY_AUTH'
    account_configs ={'aws_access_key': ACCESS_KEY,
                  'aws_secret_key': SECRET_KEY}
     api_target.create_external_account("cloudAccount1","cloudAccount1",
                               TYPE_NAME,
                               account_configs=account_configs)

        print "Peer Successfully Added"
    except ApiException as e:
        if 'already exists' in str(e):
            print 'Peer Already exists'
        else:
            raise e


    return 0

if __name__ == '__main__':
    sys.exit(main())