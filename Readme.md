## pyyaml-core - YAML 1.2 Core Schema Support for PyYAML

This module can be used on top of PyYAML to load YAML 1.2 files.

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
