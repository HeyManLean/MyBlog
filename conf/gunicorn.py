import multiprocessing
import os


bind = '0.0.0.0:5005'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'


basedir = os.path.dirname(os.path.abspath(__file__))
gunicorn_dir = os.path.join(basedir, 'gunicorn')
if not os.path.isdir(gunicorn_dir):
    os.makedirs(gunicorn_dir)
accesslog = os.path.join(gunicorn_dir, 'access.log')
errorlog = os.path.join(gunicorn_dir, 'error.log')
pidfile = os.path.join(gunicorn_dir, 'gunicorn.pid')

loglevel = 'debug'

daemon = True
