#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import yaml
import json
import os
from fire import Fire


class Parser(object):
    def load(self, string):
        raise NotImplementedError

    def dump(self, string):
        raise NotImplementedError

class JSONParser(Parser):
    def load(self, string):
        return json.loads(string)

    def dump(self, dictionary):
        return json.dumps(dictionary, indent=2)

class YamlParser(Parser):
    def load(self, string):
        return yaml.load(string)

    def dump(self, dictionary):
        return yaml.dump(dictionary, default_flow_style=False)

class SwaggerDictWrapper(object):
    def __init__(self):
        self._document = {
                "openapi": "",
                "info": "",
                "servers": [],
                "paths": {},
                "components": {},
                "security": [],
                "externalDocs": ""
        }
        self._all_keys = list(self._document.keys())

    def keys(self):
        for key in self._all_keys:
            yield key

    def put(self, key, obj):
        origin_obj = self._document[key]

        if isinstance(origin_obj, str):
            self._document[key] = obj

        if isinstance(origin_obj, list):
            self._document[key].append(obj)

        if isinstance(origin_obj, dict):
            self._document[key].update(obj)

    def remove(self, key):
        self._document.pop(key)

    @property
    def document(self):
        return self._document



class SwaggerWriter(object):

    def __init__(self, root_dir, parser):
        self._dict_wrapper = SwaggerDictWrapper()
        self._document = { "openapi": "3.0.0" }
        self._root_dir = root_dir
        self._parser = parser

    def _build(self, key):
        dirname = '%s/%s' % (self._root_dir, key)
        if not os.path.exists(dirname):
            self._dict_wrapper.remove(key)
            return
        for filename in os.listdir('%s/%s' % (self._root_dir, key)):
            fullname = '%s/%s/%s' % (self._root_dir, key, filename)
            with open(fullname) as fobj:
                self._dict_wrapper.put(key, self._parser.load(fobj.read()))

    def build_all(self):
        for key in self._dict_wrapper.keys():
            self._build(key)

    def dumps(self):
        print(self._parser.dump(self._dict_wrapper.document))

class CLI(object):
    def yaml(self, root_dir):
        writer = SwaggerWriter(root_dir, YamlParser())

        writer.build_all()
        writer.dumps()

    def json(self, root_dir):
        writer = SwaggerWriter(root_dir, JSONParser())

        writer.build_all()
        writer.dumps()

def main():
    Fire(CLI)

if __name__ == "__main__":
    main()
