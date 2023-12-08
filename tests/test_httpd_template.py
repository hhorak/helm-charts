import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmHTTPDTemplate:

    def setup_method(self):
        package_name = "httpd-template"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_package_persistent(self):
        self.hc_api.set_version("0.0.1")
        self.hc_api.package_name = "httpd-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.set_version("0.0.5")
        self.hc_api.package_name = "httpd-template"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "httpd_version": "2.4-el8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running()
        assert self.hc_api.test_helm_curl_output(
            route_name="httpd",
            expected_str="Welcome to your static httpd application on OpenShift"
        )
