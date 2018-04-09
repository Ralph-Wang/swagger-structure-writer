#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


class SwaggerWriter(object):

    def __init__(self, root_dir, parser):
        self._document = { "openapi": "3.0.0" }
        self._root_dir = root_dir
        self._parser = parser

    def build_info(self):
        for filename in os.listdir('%s/%s' % (self._root_dir, 'info')):
            fullname = '%s/%s/%s' % (self._root_dir, 'info', filename)
            with open(fullname) as fobj:
                self._document['info'] = self._parser.load(fobj.read())

    def build_servers(self):
        self._document['servers'] = []
        for filename in os.listdir('%s/%s' % (self._root_dir, 'servers')):
            fullname = '%s/%s/%s' % (self._root_dir, 'servers', filename)
            with open(fullname) as fobj:
                self._document['servers'].append(self._parser.load(fobj.read()))

    def build_paths(self):
        self._document['paths'] = {}
        for filename in os.listdir('%s/%s' % (self._root_dir, 'paths')):
            fullname = '%s/%s/%s' % (self._root_dir, 'paths', filename)
            with open(fullname) as fobj:
                self._document['paths'].update(self._parser.load(fobj.read()))

    def dumps(self):
        print(self._parser.dump(self._document))

class CLI(object):
    def yaml(self, root_dir):
        writer = SwaggerWriter(root_dir, YamlParser())

        writer.build_info()
        writer.build_servers()
        writer.build_paths()
        writer.dumps()

    def json(self, root_dir):
        writer = SwaggerWriter(root_dir, JSONParser())

        writer.build_info()
        writer.build_servers()
        writer.build_paths()
        writer.dumps()

def main():
    Fire(CLI)

if __name__ == "__main__":
    main()
