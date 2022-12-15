from multiprocessing import cpu_count

# Socket Path
bind = 'localhost:5000'
timeout = 600

# Worker Options
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/deployer/fastapi/logs/access_log'
errorlog =  '/home/deployer/fastapi/logs/error_log'