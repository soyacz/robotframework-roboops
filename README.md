# robotframework-roboops

Robot Framework's library for creating, sharing and running DevOps tasks easily and efficiently

----
Primarly designed for testers/developers who use Robot Framework.
They often create own python libraries and must maintain them.

But it's not limited only to that - you can automate any stuff with it - with syntax you know and reports you love.

# Features
- uses robotframework for running tasks - see all the benefits of robotframework
    - one that brings a lot of benefits are report and log files
- keyword for running commands
- keyword for linking artifacts into report metadata
- any failure makes remaining tasks to fail automatically (skip)
- others to come - raise your idea!

# Installation instructions
pip install robotframework-roboops

# Usage
RoboOps is typical Robotframework library - use it as usual robot library.

As this library is mainly focused on running tasks instead of tests,
try to use "\*** Tasks \***" instead of "\*** Test Cases \***" in .robot files.

This repository uses RoboOps for building, testing (and in future deploying) itself.
See pipeline.robot to see example how to do it.

This repository uses github actions - check this out to see how to use it in CI pipeline.

# Running tests
Test everything (unit tests, acceptance tests, building wheel) by running:
```
robot pipeline.robot
```
So, instead of pushing to repository and wait until your CI/CD tool
(like Jenkins/Github Actions/Travis etc.) tests if it is ok, run above command to get results 300% faster.
 
 ## running pipeline with docker (using python 3.6)
 build docker image and run it:
 ```docker build -t roboops:1.0.0 .
 docker run --rm -v "${PWD}":/code --env PYTHONPATH=. roboops:1.0.0```