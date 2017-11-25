import json
import logging

import tornado.web

from db.client import db_client
from utils import process_markdown

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """
    required_attr =[]

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = db_client()
        return self._db

    @classmethod
    def clean_post(cls, data):
        if '$$hashKey' in data:
            data.pop('$$hashKey')

        for attr in cls.required_attr:
            assert attr in blog_data and blog_data[attr], (
                'Missing attr {}'.format(attr))

    def create_markdown(self, data, attr_name, source_attr='markdown'):
        if isinstance(data[source_attr], str):
            data[attr_name] = process_markdown(data[source_attr])
        elif isinstance(data[source_attr], list):
            data[attr_name] = []
            for item in data[source_attr]:
                data[attr_name].append(
                    process_markdown(item))

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg
