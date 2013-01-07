passtools-flask
==============

A simple Passtools example app built with Flask (Python web framework) and Bootstrap. 

## Resources 

* See [passtools-python README](https://github.com/tello/passtools-python/) for more information on setting up the Passtools-Python library. 
* Indexed documentation for the python SDK is available at [http://tello.github.com/passtools-python/](http://tello.github.com/passtools-python/).

## Features

### Template API Methods

* Retrieve list of templates
* View detailed profile for each template

### Pass API Methods

* Create pass from a template
* Retrieve list of passes
* View detailed profile for each pass
* Download pass

## Roadmap

* Simple UI for editing template fields and pass fields, and saving these changes via the `update_pass` view handler. 
* SQLite database for saving preferences, such as the API key used for making requests. 
* More features that lend themselves to real-world use cases - analytics, etc.



