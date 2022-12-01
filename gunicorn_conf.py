from multiprocessing import cpu_count

# Socket Path
# bind = 'unix:/home/demo/fastapi_demo/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/fastapi/logs/access_log'
errorlog =  '/home/fastapi/logs/error_log'