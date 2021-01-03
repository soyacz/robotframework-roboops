
class TestErrorsAreFatal:

    def test_errors_are_fatal_makes_all_errors_fatal(self, robot_suite):
        test_failing = robot_suite.tests.create('Failing stage')
        test_failing.keywords.create("Fail", args=["failing due some reason"])
        test_skipped = robot_suite.tests.create('Should be skipped stage')
        test_skipped.keywords.create("Log To Console", args=["Should not execute at all"])
        result = robot_suite.run(quiet=True, output=None, log=None)

        assert result.return_code == 2, "should fail both tests"
        assert len(robot_suite.tests[1].keywords) == 0, "post failure tests should have no keywords"
