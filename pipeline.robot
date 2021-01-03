*** Settings ***
Library    RoboOps

*** Variables ***
${atest dir}     ${CURDIR}/atest    
&{install python env}    command=poetry install
&{unit tests}    command=poetry run coverage run --source=RoboOps -m pytest .
&{report coverage}    command=poetry run coverage report -m --fail-under=80
&{generate wheel}    command=poetry build
&{remove stale roboops package from atest env}    command=poetry remove robotframework-roboops    cwd=${atest dir}    ignore_rc=True
&{install atest env}    command=poetry install    cwd=${atest dir}   
&{install atest roboops package from whl}    command=poetry add ../    cwd=${atest dir}  
&{run atests}    command=poetry run robot --noncritical noncritical .    cwd=${atest dir}

*** Tasks ***
Unit Test Stage
    Roboops Run Command    &{install python env}
    Roboops Run Command    &{unit tests}
    Roboops Run Command    &{report coverage}
    
Build Package Stage
    Roboops Run Command    &{generate wheel}
    
Acceptance Test Stage
    Roboops Run Command    &{remove stale roboops package from atest env}
    Roboops Run Command    &{install atest env}
    Roboops Run Command    &{install atest roboops package from whl}
    Roboops Run Command    &{run atests}
    [Teardown]    Save Acceptance Tests Artifacts

*** Keywords ***
Save Acceptance Tests Artifacts
    Roboops Save File Artifact    ${atest dir}/log.html    atest_log.html
    Roboops Save File Artifact    ${atest dir}/report.html    atest_report.html
    Roboops Save File Artifact    ${atest dir}/output.xml    atest_output.xml
