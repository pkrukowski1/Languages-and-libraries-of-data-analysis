# Voice Assistant
## About
This is part of a project for a Python course at the AGH University of Technology. The aim of the project is to create a voice assistant that supports 
the Polish language. The project has a modular structure with many modules running in parallel and independently of each other, each implementing a different functionality (e.g.: a Timer module, a Calendar module, and a Smart Home module).
The modules can potentially run on different machines communicating with the main machine via the MQTT protocol. We use pyttsx3 for text-to-speech and SpeechRecognition for speech-to-text (the latter of which requires a network connection).

This repo contains my proposition for the main part of the project as well as some of the modules.

## Set up
To install all dependencies simply clone the repo and run:

```pip3 install -r requirements.txt```

## Running the server
To run the server with localhost as broker run:

```python3 -m src.voice_assistant_server.main <flags>```

### Available flags
- ```--broker <broker IP>``` lets you set a custom IP for the MQTT broker (by default it's set to localhost)


## Defining your module
To define a module in this architecture, define a class that extends ```src.voice_assistant_modules.va_module``` 
and override the ```process_query()``` function. Additionally, implement the ```get_id()``` classmethod to return a 
short string that will identify your module.

Your ```process_query()``` function should take in a string - the query the user asked our voice assistant, 
and return a string. The string it returns is the message the user will receive as an answer.

If your module fails to answer the question the ```process_query()``` should return ```None``` instead of a string.

## Running your module
At the end of the file add:

```
if __name__ == '__main__':
    <YourClassName>.main()
```
which upon running this file as the main script will run your class' ```main``` function. 
This will (unless you defined your own ```main``` function :D) 
call the va_module's ```main``` that will attempt to answer queries using your module's ```process_query()``` function.

To run the module, run:

```python3 -m path.to.your_module <flags>```

### Available flags
- ```--broker <broker IP>``` lets you set a custom IP for the MQTT broker (by default it's set to localhost)
- ```--log <True or False>``` setting this to True enables logging the conversations in a json file available in 
```<PROJECT_DIR>/logs```



