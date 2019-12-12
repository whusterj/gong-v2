#!/bin/bash
LOGDIR=/opt/gong/logs
LOGFILE=/opt/gong/logs/gunicorn.log
cd /opt/gong
source /opt/gongenv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec /opt/gongenv/bin/gunicorn --workers 3 \
  --bind 127.0.0.1:8000 wsgi:app \
  --log-file=$LOGFILE 2>>$LOGFILE
