echo "starting service ..."
cd service
gunicorn app.patched:app -w 1 -k gevent --bind 0.0.0.0:5001