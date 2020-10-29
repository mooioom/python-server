# python-server

## A Basic Python Server
Complete vanilla python server, no need for external libraries etc.

### Basic Features

<ol>
<li>Static Server</li>
<li>Controllers</li>
<li>Templates</li>
<li>XHR (POST)</li>
</ol>

***

### install & init

    git clone https://github.com/mooioom/python-server

And then...

    python server.py

Server is running on port 80 (default)

### routes.json
Use routes.json to define routes

    [
        {
            "uri" : "/",
            "target" : "index.html" // points to 'public' folder
        },
        {
            "uri" : "/controller",
            "controller" : "basic_controller"   // points to 'ctrl' folder
        }
    ]

### __public
Use the __public prefix in HTML to serve static files under the 'public' folder

    <img src="__public/img/image.jpg" />
    <script src="__public/js/main.js"></script>

### Templating
Data can be passed to HTML templates using double-curlies {{}}

**basic_template.html**

    <div>
        Hello {{name}}, How Are You?
    </div>

**ctrl/basic.py**

    def default( server ):
        content = server.template( 'basic_template', { 'name' : 'David' } )
        server.respond( content )

### call API - public/js/api.js
This contains a basic **call** function to XHR the server

<em>call( action_name, callback, data )</em>

including the API :<br>
    <script src="__public/js/api.js" /></script>

ex. :

    call('login', r => {
    
        if( r ) location.reload();
        
    }, {
        username : '',
        password : ''
    })

### TODOs

Some basic features left to complete

<ul>
<li>Todo :: XHR (GET)</li>
<li>Todo :: Email (SMTP Transports)</li>
<li>Todo :: Sessions</li>
</ul>