def when_ready(server):
    open('../../tmp/app-initialized', 'x').close()


bind = "0.0.0.0:$PORT"
