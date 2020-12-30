from unittest import mock

from RoboOps.RoboOps import RoboOps


class TestRunCommandKeyword:

    def test_can_execute_command_without_creating_shell(self):
        roboops = RoboOps()

        with mock.patch("subprocess.run") as mocked_subprocess_run:
            roboops.roboops_run_command("echo hello command", shell=False)
            mocked_subprocess_run.assert_called_once_with("echo hello command".split(' '),
                                                          capture_output=True, text=True, shell=False, cwd=None)

    def test_can_execute_command_with_shell(self):
        roboops = RoboOps()

        with mock.patch("subprocess.run") as mocked_subprocess_run:
            roboops.roboops_run_command("echo hello command", shell=True)
            mocked_subprocess_run.assert_called_once_with("echo hello command",
                                                          capture_output=True, text=True, shell=True, cwd=None)
