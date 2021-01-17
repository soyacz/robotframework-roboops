# robotframework-roboops

Robot Framework's library for creating, sharing and running DevOps tasks easily and efficiently.

Building pipelines with Robot Framework gives developers clear insight what CI/CD steps do
(thanks to keyword based syntax). Allow them to execute pipelines easily also on their own machines
before pushing to repository and waiting for CI/CD tool to take it up.

Thanks to nice RFWK reporting it should be easy and fast to follow pipelines and investigate issues.

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

## Example
```RobotFramework
*** Settings ***
Library    RoboOps
Library    OperatingSystem

*** Variables ***
${atest dir}     ${CURDIR}/atest    
&{install python env}    command=poetry install
&{unit tests}    command=poetry run coverage run --source=RoboOps -m pytest .
&{report coverage}    command=poetry run coverage report -m --fail-under=80
&{generate wheel}    command=poetry build
&{remove stale roboops package from atest env}    command=poetry remove robotframework-roboops    cwd=${atest dir}    ignore_rc=True
&{install atest env}    command=poetry install    cwd=${atest dir}   
&{install atest roboops package from whl}    command=poetry add ../    cwd=${atest dir}

*** Tasks ***
Unit Test Stage
    Roboops Run Command    &{install python env}
    Roboops Run Command    &{unit tests}
    Create Coverage Report And Save It
    
Build Package Stage
    Roboops Run Command    &{generate wheel}
    
Acceptance Test Stage
    Roboops Run Command    &{remove stale roboops package from atest env}
    Roboops Run Command    &{install atest env}
    Roboops Run Command    &{install atest roboops package from whl}
    Roboops Run Command    &{run atests}
    [Teardown]    Save Acceptance Tests Artifacts

*** Keywords ***
Create Coverage Report And Save It
    ${coverage}    Roboops Run Command    &{report coverage}
    Create File    coverage.log    ${coverage.stdout.decode()}
    Roboops Save File Artifact    coverage.log    coverage.log

Save Acceptance Tests Artifacts
    Roboops Save File Artifact    ${atest dir}/log.html    atest_log.html
    Roboops Save File Artifact    ${atest dir}/report.html    atest_report.html
    Roboops Save File Artifact    ${atest dir}/output.xml    atest_output.xml

```
# Running tests
Test everything (unit tests, acceptance tests, building wheel) by running:
```
robot pipeline.robot
```
So, instead of pushing to repository and wait until your CI/CD tool
(like Jenkins/Github Actions/Travis etc.) tests if it is ok, run above command to get results 300% faster.
 
 ## running pipeline with docker (using python 3.6)
 build docker image and run it:
 ```
 docker build -t roboops:latest .
 docker run --user $(id -u):$(id -g) --rm -v "${PWD}":/code --env PYTHONPATH=. roboops:latest
 ```