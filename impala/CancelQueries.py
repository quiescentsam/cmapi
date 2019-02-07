$ cat CancelQueries.py
import urllib
import json
import sys
import os
import datetime


def getHttpFormat(node):
    return "http://"+node+":25000/"


def main():
        impala_daemons_path=sys.argv[1]
        if not os.path.isfile(impala_daemons_path):
            print("File Path {0} does not exist. Exiting..".format(impala_daemons_path))
            sys.exit()
        with open(impala_daemons_path)  as f:
            content = f.readlines()
        nodes = [x.strip() for x in content]
        print(nodes)
        for i, node in enumerate(nodes):
                print("Checking {0}".format(node))
                try:
                                url = getHttpFormat(node)
                                response = urllib.urlopen(url + "queries?json")
                                data = json.loads(response.read())
                                if data["num_waiting_queries"] > 0:
                                        print(data["num_waiting_queries"])
                                        for in_flight_query in data["in_flight_queries"]:
                                                if in_flight_query["waiting"] is True and ( in_flight_query['state'] == "FINISHED" or in_flight_query['state'] == "EXCEPTION") :
                                                        cancel_url = url + "cancel_query?query_id={0}".format(in_flight_query['query_id'])
                                                        print(cancel_url)
                                                        response = urllib.urlopen(cancel_url)
                except IOError:
                        print("Skipping {0}".format(node))
                except Exception as e:
                        print(e)



if __name__ == '__main__':
    print("*****************************************************")
    print("Run Time : {0}".format(str(datetime.datetime.now())))
    main()


------ I took this and modified it to use the requests library - that allowed me to easily turn off SSL verification as well as supporting digest auth - see below.


import requests
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import json
import sys
import os
import datetime

print("*****************************************************")
print("Run Time : {0}".format(str(datetime.datetime.now())))

# Determine what Impala Daemons to contact
impala_daemons_path = sys.argv[1]
if not os.path.isfile(impala_daemons_path):
    print("File Path {0} does not exist. Exiting..".format(impala_daemons_path))
    sys.exit()
with open(impala_daemons_path) as f:
    content = f.readlines()
nodes = [x.strip() for x in content]
print(nodes)

# Contact Daemons to figure out any cancellable queries
for i, node in enumerate(nodes):
    print("Checking {0}".format(node))
    try:
        url = "https://" + node + ":25000/"
        response = requests.get(url + 'queries?json', auth = HTTPDigestAuth('foo', 'bar'), verify = False)
        data = response.json()
        if data["num_waiting_queries"] > 0:
            print(data["num_waiting_queries"])
            for in_flight_query in data["in_flight_queries"]:
                if in_flight_query["waiting"] is True and ( in_flight_query['state'] == "FINISHED" or in_flight_query['state'] == "EXCEPTION") :
                    cancel_url = url + "cancel_query?query_id={0}".format(in_flight_query['query_id'])
                    print(cancel_url)
                    # Cancel the hung query
                    response = requests.get(cancel_url, auth = HTTPDigestAuth('foo', 'bar'), verify = False)
    except IOError as e:
        print("Skipping {0}".format(node))
    except Exception as e:
        print(e)
print("*****************************************************")
