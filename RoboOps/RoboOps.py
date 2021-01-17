import subprocess
from pathlib import Path
from robot.api import logger
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.running.model import TestCase
from robot.result.model import TestCase as TestCaseResult
import shlex


class ErrorsAreFatal:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self) -> None:
        self.test_failed: bool = False

    def start_test(self, test: TestCase, result: TestCaseResult) -> None:
        logger.console("")  # just to go to next line in console at beginning
        if self.test_failed:
            test.keywords.clear()

    def end_test(self, test: TestCase, result: TestCaseResult) -> None:
        if self.test_failed:
            result.message = "Skipped execution due previous errors"
            result.status = "FAIL"  # todo: make it "SKIP" when using RF 4.0
        if not result.passed:
            self.test_failed = True

    def close(self) -> None:
        # added as unit tests somehow kept the state
        self.test_failed = False


@library(scope="TEST SUITE", version="1.0", listener=ErrorsAreFatal())
class RoboOps:
    """Library for creating, sharing and running DevOps tasks easily and efficiently.

    When is imported, any failure within a suite is fatal - preventing other steps from execution and failing whole run.

    == Example ==
    | *** Settings ***
    | Library    RoboOps

    | *** Variables ***
    | &{install python env}    command=poetry install
    | &{unit tests}    command=poetry run coverage run --source=RoboOps -m pytest .
    | &{report coverage}    command=poetry run coverage report -m --fail-under=80
    | &{generate wheel}    command=poetry build
    | *** Tasks ***
    | Unit Test Stage
    |     Roboops Run Command    &{install python env}
    |     Roboops Run Command    &{unit tests}
    |     ${coverage}    Roboops Run Command    &{report coverage}
    |     Create File    coverage.log    ${coverage.stdout.decode()}
    |     Roboops Save File Artifact    coverage.log    coverage.log
    |
    | Build Package Stage
    |     Roboops Run Command    &{generate wheel}
    """

    def __init__(self, artifacts_dir: str = "artifacts"):
        """RoboOps library can take below optional arguments:

        - ``artifacts_dir`` <str>
          Points to directory where artifacts will be stored."""
        self.artifacts_dir = Path(artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    @keyword
    def roboops_run_command(
        self,
        command: str,
        shell: bool = False,
        cwd: str = None,
        ignore_rc: bool = False,
    ) -> subprocess.CompletedProcess:
        """Runs given command using subprocess.run and returns result ``subprocess.CompletedProcess`` object.

        Arguments:
        - ``command`` <str>:
          Command to be executed.
        - ``shell`` <bool>:
          Specifies if command should be executed in separate shell (see subprocess.run documentation for more details).
          Defaults to ``False``
        - ``cwd`` <str>:
          Sets working directory for given command.
          Defaults to ``None``
        - ``ignore_rc`` <bool>:
          Ignore return code.
          By default if return code of executed command is other than 0, then keyword fails.

        """
        logger.info(
            f"running: '{command}' {'in shell' if shell else ''}", also_console=True
        )
        if not shell:
            command = shlex.split(command)  # type: ignore
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            cwd=cwd,
        )
        logger.info(result.stdout.decode())
        if result.stderr:
            logger.error(result.stderr.decode())
        if not ignore_rc:
            result.check_returncode()
        return result

    @keyword
    def roboops_save_file_artifact(self, source: Path, name: str = None) -> None:
        """
        Moves given file to ``artifacts_dir`` with given name and add to ``Artifacts`` metadata in report for easy view/download

        Arguments:
        - ``source`` <Path>: Path to file
        - ``name`` <str>: new name of the file. If not provided, original name will be used.
        """
        source = Path(source)
        name = name if name else source.name
        destination = self.artifacts_dir / name
        source.rename(destination)
        self._add_artifact_to_suite_metadata(name, destination)

    def _add_artifact_to_suite_metadata(self, name: str, file_path: Path) -> None:
        entry = f"- [{file_path}|{name}]\n"
        BuiltIn().set_suite_metadata("artifacts", entry, append=True, top=True)
