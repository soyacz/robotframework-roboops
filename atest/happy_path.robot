*** Settings ***
Documentation    happy path tests
Resource    settings.robot
Library    RoboOps    ${ARTIFACTS DIR}
Library    OperatingSystem

*** Tasks ***
Can Run Command
    Roboops Run Command    touch test_file    
    File Should Exist    test_file
    
Can Save Artifact
    Roboops Save File Artifact    test_file
    File Should Not Exist    test_file
    File Should Exist    artifacts/test_file
    