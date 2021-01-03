*** Settings ***
Documentation    one failing task should prevent from running the rest ones.
...     Execute this test with --noncritical:noncritical and --critical  critical
Library    RoboOps
Force Tags    noncritical

*** Tasks ***
First Stage
    Fail    failing this taks - next one should not execute at all
    [Teardown]    log    nothing    console=True
    
    
Second Stage
    [setup]    Remove Tags    noncritical
    Fail   this should not run at all    tags=critical 
    [teardown]    Fail    teardown should not run at all    tags=critical
    
third stage
    [setup]    Remove Tags    noncritical
    Fail   This also should not execute

