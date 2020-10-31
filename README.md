# python-server

## A Basic Python Server
Complete vanilla python server, no external libraries required

### Basic Features

<ol>
<li>Static Server</li>
<li>Controllers</li>
<li>Templates</li>
<li>SMTP Emailer</li>
<li>XHR (POST)</li>
<li>XHR (GET)</li>
</ol>

***

### install & init

    git clone https://github.com/mooioom/python-server

And then...

    python server.py <port>

Server is running on port 80 (default)

### routes.json
Use routes.json to define routes

    [
        {
            "uri" : "/controller",
            "controller" : "basic_controller"   // points to 'ctrl' folder
        }
    ]

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

Example :

    call('login', r => {
    
        if( r ) location.reload();
        
    }, {
        username : '',
        password : ''
    })

### Emailer
The SMTP emailer can be defined on server.py (defaults to Gmail)

Example :<br/>

    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 465

### TODOs

Some basic features left to complete

<ul>
<li>Todo :: Sessions</li>
</ul>