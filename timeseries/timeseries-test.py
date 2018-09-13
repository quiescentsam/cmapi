#!/usr/bin/env python2.7

import sys
import os
import argparse
from urlparse import urlparse
import time
import datetime
import json
import psycopg2
import boto
from boto.s3.key import Key
from cloudera.director.common.client import ApiClient
from cloudera.director.latest import AuthenticationApi, EnvironmentsApi, DeploymentsApi, ClustersApi
from cloudera.director.latest.models import Login
from cm_api.api_client import ApiResource
from urlparse import urlparse
from datetime import datetime, timedelta, time
from pytz import timezone

def runQuery(client, environmentName, deploymentName, clusterName, fromTime, toTime):

    cluster =ClustersApi(client).get(environmentName, deploymentName, clusterName)
    if not cluster:
        return

    #print("Cloudera Manager URL [%s]" % cluster.url)
    cluster_health = cluster.health.status
    cmUrl = urlparse(cluster.url)
    cm_host = cmUrl.hostname
    api = ApiResource(cm_host, username="admin", password="admin")

    if(cluster_health == 'NOT_AVAILABLE'):
        return;

    conn = psycopg2.connect("host=techops-meta-enc.c8ibwewzhjlc.us-east-1.rds.amazonaws.com dbname=spotfire user=spotfirerpt password=spotfire123")
    cur = conn.cursor()

    ################################Run Impala query#####################################################
    impalaQuery = "SELECT total_num_queries_rate_across_impalads WHERE entityName RLIKE  '.*CD-IMPALA.*' AND category = SERVICE"
    result = api.query_timeseries(impalaQuery, fromTime, toTime)
    ts_list = result[0]

    # Insert every points into database
    for ts in ts_list.timeSeries:
        for point in ts.data:
            cur.execute("INSERT INTO impala_usage_history (cluster_name, timestamp, average_queries) VALUES (%s, %s, %s)", (clusterName, point.timestamp, point.value))


    ################################ Run YARN query #####################################################
    yarnQuery = "SELECT apps_running_cumulative WHERE entityName RLIKE '.*root*' AND category = YARN_POOL"
    result = api.query_timeseries(yarnQuery, fromTime, toTime)
    ts_list = result[0]

    # Insert every points into database
    for ts in ts_list.timeSeries:
        for point in ts.data:
            cur.execute("INSERT INTO yarn_usage_history (cluster_name, timestamp, average_app) VALUES (%s, %s, %s)", (clusterName, point.timestamp, point.value))


    ################################Run HDFS query##################################################
    dfs_capacity_query = "SELECT dfs_capacity/(1024*1024) WHERE entityName RLIKE  '.*HDFS.*' AND category = SERVICE"
    result = api.query_timeseries(dfs_capacity_query, fromTime, toTime)
    ts_list = result[0]
    dfs_capacity = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            dfs_capacity.update({point.timestamp: point.value})

    dfs_capacity_used_query = "SELECT dfs_capacity_used/(1024*1024) WHERE entityName RLIKE  '.*HDFS.*' AND category = SERVICE"
    result = api.query_timeseries(dfs_capacity_used_query, fromTime, toTime)
    ts_list = result[0]
    dfs_capacity_used = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            dfs_capacity_used.update({point.timestamp: point.value})

    dfs_capacity_used_non_hdfs_query = "SELECT dfs_capacity_used_non_hdfs/(1024*1024) WHERE entityName RLIKE  '.*HDFS.*' AND category = SERVICE"
    result = api.query_timeseries(dfs_capacity_used_non_hdfs_query, fromTime, toTime)
    ts_list = result[0]
    dfs_capacity_used_non_hdfs = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            dfs_capacity_used_non_hdfs.update({point.timestamp: point.value})

    # Insert every points into database
    for point in dfs_capacity:
        cur.execute("INSERT INTO hdfs_usage_history (cluster_name, timestamp, dfs_capacity,dfs_capacity_used,dfs_capacity_used_non_hdfs) VALUES (%s, %s, %s, %s, %s)", (clusterName, point, float(dfs_capacity[point]),float(dfs_capacity_used[point]),float(dfs_capacity_used_non_hdfs[point])))


    ################################Run CPU query##################################################
    cpuquery = "SELECT cpu_percent_across_hosts WHERE entityName = '1' AND category = CLUSTER"
    result = api.query_timeseries(cpuquery, fromTime, toTime)
    ts_list = result[0]
    # Insert every points into database
    for ts in ts_list.timeSeries:
        for point in ts.data:
            cur.execute("INSERT INTO cpu_usage_history (cluster_name, timestamp, cpu_percent_across_hosts) VALUES (%s, %s, %s)", (clusterName, point.timestamp, point.value))


    ################################Run Network I/O query##########################################
    tbreceived_query = "SELECT total_bytes_receive_rate_across_network_interfaces where category = CLUSTER"
    result = api.query_timeseries(tbreceived_query, fromTime, toTime)
    ts_list = result[0]
    tbreceived = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            tbreceived.update({point.timestamp: point.value})

    tbtransmit_query = "SELECT total_bytes_transmit_rate_across_network_interfaces where category = CLUSTER"
    result = api.query_timeseries(tbtransmit_query, fromTime, toTime)
    ts_list = result[0]
    tbtransmit = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            tbtransmit.update({point.timestamp: point.value})

    # Insert every points into database
    for point in tbreceived:
        #print 	tbreceived[point]
        #print float(tbreceived[point])
        cur.execute("INSERT INTO network_usage_history (cluster_name, timestamp, total_bytes_receive_rate_across_network_interfaces,total_bytes_transmit_rate_across_network_interfaces) VALUES (%s, %s, %s, %s)", (clusterName, point, tbreceived[point],tbtransmit[point]))


    ###############################Run HDFS I/O query#################################################
    tbreadrate_query = "select total_bytes_read_rate_across_datanodes where category = SERVICE and serviceType = HDFS"
    result = api.query_timeseries(tbreadrate_query, fromTime, toTime)
    ts_list = result[0]
    tbreadrate = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            tbreadrate.update({point.timestamp: point.value})

    tbwrittenrate_query = "select total_bytes_written_rate_across_datanodes where category = SERVICE and serviceType = HDFS"
    result = api.query_timeseries(tbwrittenrate_query, fromTime, toTime)
    ts_list = result[0]
    tbwrittenrate = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            tbwrittenrate.update({point.timestamp: point.value})

    # Insert every points into database
    for point in tbreadrate:
        cur.execute("INSERT INTO hdfsio_usage_history (cluster_name, timestamp, total_bytes_read_rate_across_datanodes,total_bytes_written_rate_across_datanodes) VALUES (%s, %s, %s, %s)", (clusterName, point, tbreadrate[point],tbwrittenrate[point]))

    ###############################Run Memory query#################################################
    memoryused_query = "select physical_memory_used WHERE category = HOST"
    result = api.query_timeseries(memoryused_query, fromTime, toTime)
    ts_list = result[0]
    memoryused = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            memoryused.update({point.timestamp: point.value})

    memorytotal_query = "select physical_memory_total WHERE category = HOST"
    result = api.query_timeseries(memorytotal_query, fromTime, toTime)
    ts_list = result[0]
    memorytotal = {}
    # Insert every points into dictionary
    for ts in ts_list.timeSeries:
        for point in ts.data:
            memorytotal.update({point.timestamp: point.value})

    # Insert every points into database
    for point in memoryused:
        cur.execute("INSERT INTO memory_usage_history (cluster_name, timestamp, physical_memory_used,physical_memory_total) VALUES (%s, %s, %s, %s)", (clusterName, point, memoryused[point],memorytotal[point]))

    # Commit and close connections
    conn.commit()
    cur.close()
    conn.close()


def main(arguments):

    # Get all command line arguments

    cloudera_director_server = arguments[0]
    admin_username = arguments[1]
    credentials_file_path = arguments[2]
    admin_password = open(credentials_file_path, 'r').read()
    num_lookback_dates = arguments[3]

    # Optional arguments for transient clusters
    cluster_name = ''
    if((len(arguments)) > 4):
        cluster_name = arguments[4]

    # Setup a Cloudera Director Client
    client = ApiClient(cloudera_director_server)
    AuthenticationApi(client).login(Login(username=admin_username, password=admin_password))

    # Get all Environments
    environments = EnvironmentsApi(client).list()
    if not environments:
        sys.exit(1)

    # Get start and end time of the query
    local_tz = timezone('US/Eastern')
    from_time = datetime.now() - timedelta(hours=8)
    from_time = from_time.replace(tzinfo=local_tz)
    to_time = datetime.now().replace(tzinfo=local_tz)

    # Iterate through all environments to get all deployments
    for environment in environments:
        deployments = DeploymentsApi(client).list(environment)
        if not deployments:
            continue

        # Iterate through all deployments to get all clusters
        for deployment in deployments:
            clusters = ClustersApi(client).list(environment, deployment)
            if not clusters:
                continue

            # Iterate through all clusters to run queries
            for cluster in clusters:
                #Filter only the cluster if cluster name passed as argument
                if(cluster_name != '' and cluster_name != cluster):
                    continue

                print("Get the usage of cluster [%s] in deployment [%s] in environment [%s] from [%s] to [%s] " % (cluster, deployment, environment,from_time,to_time))
                runQuery(client, environment, deployment, cluster, from_time, to_time)


            # Iterate through each lookbackDate
            # Note: If pass in the from_time = today - num_lookback_dates, to_time = today. Cloudera Manager will return points group by longer time frame, ex hours.
            #       So the approach here is trying to pass in 24 hours in each query, so that Cloudera Manager will return points every 10 minutes.
            # for x in range(int(num_lookback_dates), 0, -1):
            # lookbackDate = datetime.datetime.utcnow().date()-datetime.timedelta(days=x)
            # from_time = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.combine(lookbackDate, datetime.time.min).timetuple())).replace(tzinfo=local_tz)
            # to_time = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.combine(lookbackDate, datetime.time.max).timetuple())).replace(tzinfo=local_tz)

            # print("Get the usage of cluster [%s] in deployment [%s] in environment [%s] from [%s] to [%s] " % (cluster, deployment, environment,from_time,to_time))
            # try:
            # runQuery(client, environment, deployment, cluster, from_time, to_time)
            # except:
            # print("Could not get usage for cluster [%s] in deployment [%s] in environment [%s] from [%s] to [%s] " % (cluster, deployment, environment,from_time,to_time))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
