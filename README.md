Overhear
========

A monitoring device

Architecture
------------

- RasPi continually records 10s samples, analyze for interesting audio, if so, upload to s3 bucket and report to server.
- Server, receiving the request, creates an mturk HIT, with link to s3.
- A cron process checks HITs for completions. If it finds one, it takes the result and posts to twitter.



Installation
------------

Python >=3.3

requires housepy

    sudo pip-3.3 install -r requirements.txt

    sudo apt-get install monit

Notes
-----

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




### Copyright/License

Copyright (c) 2013 Brian House

This code is released under the MIT License and is completely free to use for any purpose. See the LICENSE file for details.

