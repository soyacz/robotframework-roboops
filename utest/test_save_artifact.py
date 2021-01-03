from pathlib import Path
from unittest.mock import patch
from RoboOps.RoboOps import RoboOps


class TestSaveFileArtifact:

    @patch("RoboOps.RoboOps._add_artifact_to_suite_metadata")
    def test_save_file_artifact_moves_it_to_artifacts_dir(self, add_to_metadata_func, artifacts_dir, test_artifact):
        roboops = RoboOps(artifacts_dir=artifacts_dir)
        roboops.roboops_save_file_artifact(source=test_artifact)

        assert Path(f"{artifacts_dir}/{test_artifact}").exists()

    @patch("RoboOps.RoboOps._add_artifact_to_suite_metadata")
    def test_save_file_artifact_moves_it_to_artifacts_dir_with_new_name(self, add_to_metadata_func, artifacts_dir,
                                                                        test_artifact):
        roboops = RoboOps(artifacts_dir=artifacts_dir)
        roboops.roboops_save_file_artifact(source=test_artifact, name="new_artifact_name.txt")

        assert Path(f"{artifacts_dir}/new_artifact_name.txt").exists()

    def test_saving_artifact_add_link_to_report(self, test_artifact, artifacts_dir, robot_suite):
        test = robot_suite.tests.create('Testing')
        test.keywords.create("RoboOps Save File Artifact", args=[test_artifact])
        result = robot_suite.run(quiet=True, output=None, log=None)

        assert Path(f"{artifacts_dir}/{test_artifact}").exists()
        assert result.suite.metadata["artifacts"] == f"- [{artifacts_dir}/{test_artifact}|{test_artifact}]\n"

    def test_saving_artifact_add_link_to_report_twice(self, test_artifact, artifacts_dir, robot_suite):
        second_artifact_path = 'test_artifact_second.txt'
        open(second_artifact_path, 'a').close()
        test = robot_suite.tests.create('Testing')
        test.keywords.create("RoboOps Save File Artifact", args=[test_artifact])
        test.keywords.create("RoboOps Save File Artifact", args=[second_artifact_path])
        result = robot_suite.run(quiet=True, output=None, log=None)

        assert Path(f"{artifacts_dir}/{test_artifact}").exists()
        assert result.suite.metadata["artifacts"] == f"- [{artifacts_dir}/{test_artifact}|{test_artifact}]\n" \
                                                     f" - [{artifacts_dir}/{second_artifact_path}|{second_artifact_path}]\n"
