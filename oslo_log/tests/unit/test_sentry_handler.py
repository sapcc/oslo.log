from unittest.mock import patch
from oslotest import base as test_base
from oslo_log.sentry import SentryHandler
import sentry_sdk


class SentryHandlerTest(test_base.BaseTestCase):

    def setUp(self):
        super(SentryHandlerTest, self).setUp()

    @patch.object(sentry_sdk, 'init', return_value=None)
    def test_init_sdk_called(self, mock_init):
        SentryHandler()
        mock_init.assert_called_once()

    def test_init_sdk_not_called(self):
        self.assertEqual(SentryHandler.is_client_initialized(), False)

    @patch.object(sentry_sdk.integrations.logging.EventHandler, 'emit')
    def test_logging_error_message(self, mock_emit):
        import logging

        logger = logging.getLogger('test_logger')
        logger.setLevel(logging.ERROR)

        sentry_handler = SentryHandler()
        sentry_handler.setLevel(logging.ERROR)

        logger.addHandler(sentry_handler)

        logger.error("Test Message")
        mock_emit.assert_called_once()
