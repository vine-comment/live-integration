source /root/vine/bin/activate
# NOTE: This script will kill all django processes.
pkill -f 'python manage.py runserver 0.0.0.0:8088'
export PYTHONIOENCODING=utf-8
python manage.py runserver 0.0.0.0:8088
ps aux | grep --color \[m\]anage\.py
