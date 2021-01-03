import shutil
from pytest import fixture
from robot.api import TestSuite


@fixture(scope="session")
def artifacts_dir():
    return "artifacts"


@fixture(scope="function", autouse=True)
def cleanup_artifacts_dir(artifacts_dir):
    shutil.rmtree(artifacts_dir, ignore_errors=True)


@fixture(scope="function")
def test_artifact():
    artifact_path = 'test_artifact.txt'
    open(artifact_path, 'a').close()
    return artifact_path


@fixture(scope="function")
def robot_suite(artifacts_dir):
    suite = TestSuite('RoboOps Test Suite')
    suite.resource.imports.library('RoboOps', args=[artifacts_dir])
    return suite

