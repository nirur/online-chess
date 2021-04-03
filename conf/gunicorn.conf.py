def when_ready(server):
    open('../../tmp/app-initialized', 'x').close()


bind = "unix:///tmp/nginx.socket"
