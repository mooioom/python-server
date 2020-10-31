# API email tester demo

def default( server, postData = None, getData = None ):

    print("email tester")

    server.email( postData['to'], 'Test Subject', 'Test Body' )

    server.respondJson( True )