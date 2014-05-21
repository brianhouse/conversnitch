Conversnitch
============

by Brian House and Kyle McDonald

Conversnitch is a small device that automatically tweets overheard conversations, bridging the gap between (presumed) private physical space and public space online.

Information moves between spaces that might be physical or virtual, free or proprietary, illegal or playful, spoken or transcribed.


Instructions
------------
Should run continuously; power-up is automatic, must have continuous
access to an internet-connected wireless network.


Architecture
------------

- RasPi continually records 10s samples, analyze for interesting audio, if so, upload to s3 bucket and report to server.
- Server, receiving the request, creates an mturk HIT, with link to s3.
- A cron process checks HITs for completions. If it finds one, it takes the result and posts to twitter.


Installation
------------

requires Python >=3.3  
requires housepy  
requires monit (follow instructions in monit_server)  

    sudo apt-get install monit
    sudo pip-3.3 install -r requirements.txt


mturk urls
----------

https://mturk.com/  
https://requester.mturk.com/  
https://requestersandbox.mturk.com/  
https://workersandbox.mturk.com/  


Server reminders
----------------
    cp ngnix.conf /etc/nginx/
    sudo service nginx start

    scp -i overhear.pem ubuntu@54.235.200.47:~/overhear/config.yaml config.yaml

make sure the server is on top of the time:

    tzselect
    sudo apt-get install ntp


RasPI reminders
---------------
    alsamixer


### Copyright/License

Copyright (c) 2013 Brian House and Kyle McDonald

This code is released under the MIT License and is completely free to use for any purpose. See the LICENSE file for details.

