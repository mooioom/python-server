def default( server ):

    content = server.template( 'basic_template', { 'hello' : 1 } )
    server.respond( content )
