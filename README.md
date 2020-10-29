# python-server

## A Basic Server Application

### Features

<ol>
<li>Static Server</li>
<li>Controllers</li>
<li>Templates</li>
<li>POST API</li>
</ol>

### routes.json

Use routes.json to define routes

    [
        {
            "uri" : "/",
            "target" : "index.html"
        },
        {
            "uri" : "/controller",
            "controller" : "basic_controller"
        }
    ]

### __public

Use the __public prefix in HTML to serve static files under the 'public' folder

    <img src="__public/img/image.jpg" />
    <script src="__public/js/main.js"></script>
    