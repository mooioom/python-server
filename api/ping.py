# API controller demo

def default( server, data ):

    print("ping::defualt")

    server.respondJson(data)

def sub_method( server, data ):

    server.respondJson(True)