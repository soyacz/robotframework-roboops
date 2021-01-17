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
&{run atests}    command=poetry run robot --noncritical noncritical .    cwd=${atest dir}
&{get package version}    command=poetry version -s
${PACKAGE URL}    https://pypi.org/pypi/robotframework-roboops/json

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

Static Type Checks
    Roboops Run Command    poetry run mypy RoboOps

Validate Files Formatting
    [Documentation]    If fails run "poetry run black ."
    Roboops Run Command    poetry run black --check -q .

Validate Version
    ${current version}    Get Current RoboOps Version
    ${pypi versions}    Get Released Versions From PyPi
    Should Not Be True     $current_version in $pypi_versions
    ...    msg=This version already exists. Did you forget bump up the RoboOps version?

*** Keywords ***
Create Coverage Report And Save It
    ${coverage}    Roboops Run Command    &{report coverage}
    Create File    coverage.log    ${coverage.stdout.decode()}
    Roboops Save File Artifact    coverage.log

Save Acceptance Tests Artifacts
    Roboops Save File Artifact    ${atest dir}/log.html    atest_log.html
    Roboops Save File Artifact    ${atest dir}/report.html    atest_report.html
    Roboops Save File Artifact    ${atest dir}/output.xml    atest_output.xml

Get Current RoboOps Version
    ${result}    Roboops Run Command    &{get package version}
    [Return]    ${{$result.stdout.decode()[:-1]}}

Get Released Versions From PyPi
    ${result}    Roboops Run Command    curl -s ${PACKAGE URL}
    ${pypi versions}    Set Variable    ${{json.loads($result.stdout.decode())["releases"].keys()}}
    Should Not Be Empty    ${pypi versions}    Couldn't get releases from pypi
    [Return]    ${pypi versions}