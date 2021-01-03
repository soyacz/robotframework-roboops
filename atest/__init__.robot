*** Settings ***
Resource    settings.robot
Library    OperatingSystem
Suite Setup    Remove Directory    ${ARTIFACTS DIR}    recursive=True
