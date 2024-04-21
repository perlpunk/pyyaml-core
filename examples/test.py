import yaml
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from yamlcore import CoreLoader, CCoreLoader, CoreDumper, CCoreDumper


class MyCoreLoader(CoreLoader):
    pass


def foo_constructor(c, node):
    value = c.construct_scalar(node)
    return value.upper()


MyCoreLoader.add_constructor('!foo', foo_constructor)

y = """
---
1.1: # strings
- yes
- no # norway problem anymore
- 1__0
- 10:20
- +0b100
- 0x4_2

core:
- true
- 0o10
- 0x42
- ~
- .inf
"""

print("============ SafeLoader")
d = yaml.load(y, Loader=yaml.SafeLoader)
print(d)

print("============ SafeDumper")
out = yaml.dump(d, Dumper=yaml.SafeDumper)
print(out)

print("============ CoreLoader")
d = yaml.load(y, Loader=CoreLoader)
print(d)

print("============ CoreDumper")
out = yaml.dump(d, Dumper=CoreDumper)
print(out)

print("============ MyCoreLoader")
y2 = """
!foo bar
"""
d = yaml.load(y2, Loader=MyCoreLoader)
print(d)


# print("========== PyYAML")
# d = yaml.safe_load("!!null foo")
# print(d)
