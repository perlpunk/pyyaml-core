## pyyaml-core - YAML 1.2 Core Schema Support for PyYAML

This module can be used on top of PyYAML to load YAML 1.2 files.

Currently it supports enabling all YAML 1.2 Core Schema tags on top
of the PyYAML BaseLoader.

For more information see the [comparison of 1.1 and 1.2
schemas](https://perlpunk.github.io/yaml-test-schema/schemas.html).

## Examples

    import yaml
    from yamlcore.loader import CoreLoader
    from yamlcore.dumper import CoreDumper

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

    d = yaml.load(y, Loader=CoreLoader)
    out = yaml.dump(d, Dumper=CoreDumper)

You can also use `CCoreLoader` and `CCoreDumper` for using the
[libyaml](https://github.com/yaml/libyaml) based parser and emitter.

## Why?

At the time of this writing, there is a [pending pull
request](https://github.com/yaml/pyyaml/pull/555) that adds YAML 1.2 Core
Schema Support for PyYAML.

It's blocked because there is a plan to redesign the API, and no new things
shall be added using the old API at this point.

So as long as PyYAML doesn't merge this, you can use this module as an
alternative.
