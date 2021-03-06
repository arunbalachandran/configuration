#!/usr/bin/env python3.6
"""Simple utility for deciphering Ansible jsonized task output."""

from __future__ import absolute_import
from __future__ import print_function
import json
import sys

if len(sys.argv) > 1:
    f = open(sys.argv[1])
else:
    if sys.stdin.isatty():
        print("Copy one complete line of junk from ansible output, and pipe it to me.")
        sys.exit()
    f = sys.stdin

junk = f.read()

# junk:
# '==> default: failed: [localhost] (item=/edx/app/edx_ansible/edx_ansible/requirements.txt) => {"cmd": "/edx/app/edx...'

print(("Stdin is {} chars: {!r}...{!r}".format(len(junk), junk[:40], junk[-40:])))

junk = junk.replace('\n', '')
junk = junk[junk.index('=> {')+3:]
junk = junk[:junk.rindex('}')+1]

data = json.loads(junk)

GOOD_KEYS = ['cmd', 'msg', 'stdout', 'stderr', 'module_stdout', 'module_stderr', 'warnings']
IGNORE_KEYS = ['stdout_lines', 'stderr_lines', 'start', 'end', 'delta', 'changed', 'failed', 'rc', 'item']

for key in GOOD_KEYS:
    if data.get(key):
        print(f"== {key} ===========================")
        print((data[key]))

unknown_keys = set(data) - set(GOOD_KEYS) - set(IGNORE_KEYS)
if unknown_keys:
    print("== Unknown keys ======================")
    for key in unknown_keys:
        print(f"{key}: {data[key]!r:80}")
