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
