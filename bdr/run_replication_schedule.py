cmd = hdfs.trigger_replication_schedule(schedule.id)



cmd = cmd.wait()
result = hdfs.get_replication_schedule(schedule.id).history[0].hdfsResult
