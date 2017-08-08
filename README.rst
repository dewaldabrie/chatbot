Chatbot Server
=============
This web app is a chat server that enables a single user to chat with a bot. 
The current bot implementation is a simple scripted bot (no AI).

Installation
============
Clone the repo to your computer. 
Make sure you have Python2.7 installed together with pip.
Change directory to the chatbot folder and run::

  $ pip install -r requirements.txt
    
Running the application locally
===============================
There are some fixtures defined with a basic questionare for the bot to follow.
To run this, use the testserver and load the fixture::

  $ python manage.py testserver	basic_background_questionaire.yaml
  
Browse to localhost:8000 and have a nice chat!


Additional features to add
==========================
The following can be added:

* Pin requirements with something like pip compile
* Expand functional tests
* Add unit tests
* Make use of django base template
* Upgrade look and feel
* Use AJAX calls in UI
* Use websockets instead of HTTP (django channels)
* Have multiple configurable bots
* Create AI bot
