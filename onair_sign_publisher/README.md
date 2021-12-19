# Onair Sign Publisher

Simple application that reads (from the registry) whether the computers webcam 
or microphone are currently used by an application and publishes this information via http to a configurable webserver.

The main purpose is to use it in combination with an onair sign to make people aware that one is in an active web 
conference (Zoom, Teams, Skype, etc.)

## Setup environment

To setup a development environment and install all requirements run the following commands (example for windows):

    python -m venv venv
    venv/Scripts/activate
    python -m pip install -r requirements.txt

## Build stand-alone executable

    python setup.sh pyinstaller

## Run publisher

Make sure you have the *config.json* file in the root folder of the project or in the same folder as the stand-alone 
binary. Fill in the correct endpoint of the webserver that should receive the information and you're good to go.