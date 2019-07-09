import urllib2, json

#import ssl

#ctx = ssl.create_default_context()

#ctx.check_hostname = False

#ctx.verify_mode = ssl.CERT_NONE

datanodes = ["http://pslva069.vanguard.com:25000/",
             "http://pslva060.vanguard.com:25000/",
             "http://pslva142.vanguard.com:25000/",
             "http://pslva058.vanguard.com:25000/",
             "http://pslva141.vanguard.com:25000/",
             "http://pslva097.vanguard.com:25000/",
             "http://pslva146.vanguard.com:25000/",
             "http://pslva056.vanguard.com:25000/",
             "http://pslva144.vanguard.com:25000/",
             "http://pslva077.vanguard.com:25000/",
             "http://pslva138.vanguard.com:25000/",
             "http://pslva096.vanguard.com:25000/",
             "http://pslva059.vanguard.com:25000/",
             "http://pslva139.vanguard.com:25000/",
             "http://pslva066.vanguard.com:25000/",
             "http://pslva134.vanguard.com:25000/",
             "http://pslva140.vanguard.com:25000/",
             "http://pslva126.vanguard.com:25000/",
             "http://pslva061.vanguard.com:25000/",
             "http://pslva070.vanguard.com:25000/",
             "http://pslva129.vanguard.com:25000/",
             "http://pslva068.vanguard.com:25000/",
             "http://pslva127.vanguard.com:25000/",
             "http://pslva137.vanguard.com:25000/",
             "http://pslva095.vanguard.com:25000/",
             "http://pslva078.vanguard.com:25000/",
             "http://pslva133.vanguard.com:25000/",
             "http://pslva135.vanguard.com:25000/",
             "http://pslva143.vanguard.com:25000/",
             "http://pslva132.vanguard.com:25000/",
             "http://pslva093.vanguard.com:25000/",
             "http://pslva055.vanguard.com:25000/",
             "http://pslva128.vanguard.com:25000/",
             "http://pslva145.vanguard.com:25000/",
             "http://pslva131.vanguard.com:25000/",
             "http://pslva136.vanguard.com:25000/",
             "http://pslva062.vanguard.com:25000/",
             "http://pslva057.vanguard.com:25000/",
             "http://pslva130.vanguard.com:25000/",
             "http://pslva064.vanguard.com:25000/",
             "http://pslva065.vanguard.com:25000/",
             "http://pslva076.vanguard.com:25000/",
             "http://pslva067.vanguard.com:25000/",
             "http://pslva063.vanguard.com:25000/"]

for i, datanode in enumerate(datanodes):
    print("Checking {}: {}".format(i, datanode))
    try:
        #response = urllib2.urlopen(datanode + "queries?json", context=ctx)
        response = urllib2.urlopen(datanode + "queries?json")
        data = json.loads(response.read())

        #print(data)

        if data["num_waiting_queries"] > 0:
            print(data["num_waiting_queries"])
            for in_flight_query in data["in_flight_queries"]:
                if in_flight_query["waiting"] is True and in_flight_query['state'] in ['FINISHED', 'EXCEPTION'] :
                    cancel_url = datanode + "cancel_query?query_id={}".format(in_flight_query['query_id'])
                    print(cancel_url)
                    response = urllib2.urlopen(cancel_url)

    except IOError:
        print("Skipping {}: {}".format(i, datanode))



    except Exception as e:

        print(e)

