from multiprocessing import cpu_count

# Socket Path
# bind = 'unix:/home/demo/fastapi_demo/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/deployer/fastapi/logs/access_log'
errorlog =  '/home/deployer/fastapi/logs/error_log'