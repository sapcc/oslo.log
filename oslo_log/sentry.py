import sentry_sdk

from sentry_sdk.consts import VERSION
from sentry_sdk.integrations.logging import EventHandler, BreadcrumbHandler


def version_to_tuple(version):
    return tuple(map(int, version.split('.')))


class SentryHandler(EventHandler):
    """
    The Sentry library 'raven' is long deprecated.
    Relying on the new standard Sentry EventHandler does not work, as compared to 'raven', no Sentry client is initialized
    To overcome this, a decision was made to mimic the 'raven' behavior with a custom Eventhandler
    """
    def __init__(self):
        super().__init__()
        if not self.is_client_initialized():
            # There is no need to use the default Sentry LoggingIntegration for our usecase
            # According to the source code the integration overwrites the callHandlers of standard logging library
            # logging.Logger.callHandlers = sentry_patched_callhandlers
            # Source: https://github.com/getsentry/sentry-python/blob/200d0cdde8eed2caa89b91db8b17baabe983d2de/sentry_sdk/integrations/logging.py#L111
            # It is enough to configure the Handler sentry_sdk.integrations.logging.EventHandler via log.ini
            # Calling the handler happens via the standard python logging library makes sure the Eventhandler
            sentry_sdk.init(
                integrations=[],
                # disable all default integrations (e.g. sentry_sdk.integrations.excepthook.ExcepthookIntegration)
                default_integrations=False,
                # disable all auto enabling integrations (e.g. sentry_sdk.integrations.flask.FlaskIntegration)
                auto_enabling_integrations=False,
                debug=False,
            )

    @staticmethod
    def is_client_initialized():
        if version_to_tuple(VERSION) > version_to_tuple('1.45.1'):
            return True if sentry_sdk.get_client() is not None else False
        else:
            hub = sentry_sdk.Hub.current
            return True if hub.client is not None else False
