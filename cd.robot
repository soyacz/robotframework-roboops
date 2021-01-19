*** Settings ***
Library    RoboOps

*** Variables ***
&{publish package}    command=poetry publish -n

*** Tasks ***
Publish New Version
    Roboops Run Command    &{publish package}
