from unittest.mock import patch

import requests
from openwisp_utils import utils
from openwisp_utils.tests import TimeLoggingTestRunner

success_response = requests.Response()
success_response.status_code = 204
# Captured at import time, before the runner mocks "post", so that tests
# can restore it in any process regardless of the multiprocessing start
# method (Python 3.14 defaults to "forkserver" on Linux, where test
# workers no longer inherit attributes set on the class by the parent).
original_post = requests.Session.post


class MockRequestPostRunner(TimeLoggingTestRunner):
    """This runner ensures that usage metrics are not sent in development when running tests."""

    pass

    def setup_databases(self, **kwargs):
        with patch.object(
            utils.requests.Session, "post", return_value=success_response
        ):
            return super().setup_databases(**kwargs)

    def run_suite(self, suite, **kwargs):
        with patch.object(
            utils.requests.Session, "post", return_value=success_response
        ):
            return super().run_suite(suite)
