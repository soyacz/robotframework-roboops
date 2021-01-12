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


@library(
    scope="TEST SUITE", version="1.0", doc_format="reST", listener=ErrorsAreFatal()
)
class RoboOps:
    def __init__(self, artifacts_dir: str = "artifacts"):
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
        source = Path(source)
        name = name if name else source.name
        destination = self.artifacts_dir / name
        source.rename(destination)
        self._add_artifact_to_suite_metadata(name, destination)

    def _add_artifact_to_suite_metadata(self, name: str, file_path: Path) -> None:
        entry = f"- [{file_path}|{name}]\n"
        BuiltIn().set_suite_metadata("artifacts", entry, append=True, top=True)
