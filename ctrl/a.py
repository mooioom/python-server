def default( server ):

    content = server.template( 'test', { 'hello' : 1 } )

    server.respond( content )
