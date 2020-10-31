# API controller demo

def default( server, postData = None, getData = None ):

    print("ping::defualt")

    server.respondJson(postData)

def sub_method( server, postData ):

    server.respondJson(True)