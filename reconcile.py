#!/usr/bin/env /usr/bin/python3

from requests import get
import json
import yaml
import sys
import os
from configparser import ConfigParser

#import pdb; pdb.set_trace()

url = 'http://localhost:8123/api/states'

headers = {'x-ha-access': '',
           'content-type': 'application/json'}
parser = ConfigParser()
parser.read(os.path.expanduser('~/.homeassistant.ini'))
headers['x-ha-access'] = parser.get('api','password')

response = get(url, headers=headers)
if response.ok != True:
    print("Error on request to <<%s>>: <<%s>>" % (url, response.reason) , file=sys.stderr)
    sys.exit(1)

val = json.loads(response.text)
print("\nNum Entities: %u\n" % len(val))

entities = set()
for v in val:
    entities.add(v['entity_id'])

class IgnoreInclude(yaml.Loader):
    def __init__(self, stream):
        super(IgnoreInclude, self).__init__(stream)
    def include(self, node):
        return dict(entities= '')
IgnoreInclude.add_constructor('!include', IgnoreInclude.include)

with open("group.yaml", 'r') as stream:
    groups = yaml.load(stream, IgnoreInclude)

gentities = set()
for group in groups:
    if group != None:
        for gid in groups[group]['entities']:
            gentities.add(gid)

# This is the entities that have no group
print("Untracked entities: %s\n" % list(entities - gentities))
# This is the entities that have a group but don't exist in system
print("Stale entities: %s\n" % list(gentities - entities))

untracked = dict(
  name = 'untracked',
  view = 'yes',
  entities = list(entities - gentities)
)

with open('untracked.yaml', 'w') as outfile:
    yaml.dump(untracked, outfile, default_flow_style=False)

