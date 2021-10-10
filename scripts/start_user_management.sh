clear
echo "starting user management ..."
cd user_management
gunicorn app.patched:app -w 1 -k gevent --bind 0.0.0.0:5000