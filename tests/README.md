From the main Project directory, you can run the following to run the tests: 

``` 
pipenv run python -m unittest discover tests/
```

To run tests, you first need to create a test auth config in 'tests/test_config.cfg',
to interact with hydra using user cardentals.

```
[ocm]
token = TOKEN
```
- Follow this [process](https://gitlab.cee.redhat.com/erjones/openCasesTelemetry#setup) to get a **token**. 

You can controll the test run behavior by using one of the following ENV variables

Example:
```
export DEBUG_TESTING=True
```

Variable for Controlling Test Behavior:

1. DEBUG_TESTING: options(True,False) - Used to turn on printing of data (not actual tests).
1. DEBUG_INDENT_NUMBER: option(# Numeric Value) - Number of Spaces to indent json (pretty printing).
1. DEBUG_ACCOUNT_NUMBER: optoin(# String Value) - Account Number to used in the tests.
1. DEBUG_ORG_ID: option(# String Value) - OCM org_id HAHS used in the tests.
1. DEBUG_CREATOR_ID: option(# String Value) - OCM creator_id used in the tests.
1. DEBUG_CLUSTER_ID: option(# String Value) - OpenShift Cluster UUID used in the tests
    - requires cluter to report telemetry or subscription information to ocm.
