import json
import logging.config
import plaster
from pyramid.decorator import reify


class JsonLoader(plaster.ILoader):
    def __init__(self, uri):
        self.uri = uri

    @reify
    def _loaded(self):
        return json.load(open(self.uri.path))

    def get_sections(self):
        return set(self._loaded.keys())

    def get_settings(self, section=None, defaults=None):
        val = {}
        if defaults is not None:
            val.update(defaults)
        if section is None:
            section = self.uri.fragment
        val.update(self._loaded[section])
        return val

    def setup_logging(self, defaults=None):
        val = {}
        if defaults is not None:
            val.update(defaults)
        val.update(self._loaded['logging'])
        logging.config.dictConfig(val)
