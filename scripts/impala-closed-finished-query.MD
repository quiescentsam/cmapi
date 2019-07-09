python impala-close-finished-queries.py
or
python impala-close-finished-queries.py > /tmp/impala-cleanup.out 2>&1 &
tail -f /tmp/impala-cleanup.out 
tail -f /tmp/impala-cleanup.out

After testing that it runs fine, put it on a crontab job to run every 5 minutes, for instance.