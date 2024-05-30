import yaml
import re
import collections.abc


class CommonResolver(yaml.resolver.BaseResolver):

    @classmethod
    def init_resolvers(cls, key):
        for args in _resolvers[key]:
            cls.add_implicit_resolver(
                'tag:yaml.org,2002:' + args[0],
                args[1], args[2]
            )


class CommonConstructor(yaml.constructor.BaseConstructor):

    inf_value = 1e300
    while inf_value != inf_value*inf_value:
        inf_value *= inf_value
    nan_value = -inf_value/inf_value   # Trying to make a quiet NaN (like C99).

    bool_values = {
        'core': {
            'true':     True,
            'True':     True,
            'TRUE':     True,
            'false':    False,
            'False':    False,
            'FALSE':    False,
        },
    }

    def construct_yaml_bool_core(self, node):
        value = self.construct_scalar(node)
        return self.bool_values["core"][value]

    null_values = {
        'core': {
            '':     None,
            '~':    None,
            'null': None,
            'Null': None,
            'NULL': None,
        },
    }

    def construct_yaml_null_core(self, node):
        value = self.construct_scalar(node)
        return self.null_values["core"][value]

    def construct_yaml_int_core(self, node):
        value = self.construct_scalar(node)
        sign = +1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]

        if value == '0':
            return 0
        elif value.startswith('0o'):
            return sign*int(value[2:], 8)
        elif value.startswith('0x'):
            return sign*int(value[2:], 16)
        else:
            return sign*int(value)

    def construct_yaml_float_core(self, node):
        value = self.construct_scalar(node)
        value = value.lower()
        sign = +1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]
        if value == '.inf':
            return sign*self.inf_value
        elif value == '.nan':
            return self.nan_value
        else:
            return sign*float(value)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise yaml.constructor.ConstructorError("while constructing a mapping", node.start_mark,
                        "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found duplicate key", key_node.start_mark
                )
            mapping[key] = value
        return mapping

    @classmethod
    def init_constructors(cls, tagset):
        if tagset not in _constructors:
            return
        for key in _constructors[tagset]:
            callback = _constructors[tagset][key]
            if (key is None):
                cls.add_constructor(key, callback)
            else:
                cls.add_constructor('tag:yaml.org,2002:' + key, callback)


_constructors = {
    'core':  {
        'str': yaml.constructor.SafeConstructor.construct_yaml_str,
        'seq': yaml.constructor.SafeConstructor.construct_yaml_seq,
        'map': yaml.constructor.SafeConstructor.construct_yaml_map,
        None: yaml.constructor.SafeConstructor.construct_undefined,
        'int': CommonConstructor.construct_yaml_int_core,
        'float': CommonConstructor.construct_yaml_float_core,
        'null': CommonConstructor.construct_yaml_null_core,
        'bool': CommonConstructor.construct_yaml_bool_core,
    },
}

_resolvers = {
    'core': [
        ['bool',
            re.compile(r'''^(?:|true|True|TRUE|false|False|FALSE)$''', re.X),
            list('tTfF')],
        ['int',
            re.compile(r'''^(?:
                    |0o[0-7]+
                    |[-+]?(?:[0-9]+)
                    |0x[0-9a-fA-F]+
                    )$''', re.X),
            list('-+0123456789')],
        ['float',
            re.compile(r'''^(?:[-+]?(?:\.[0-9]+|[0-9]+(\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?
                    |[-+]?\.(?:inf|Inf|INF)
                    |\.(?:nan|NaN|NAN))$''', re.X),
            list('-+0123456789.')],
        ['null',
            re.compile(r'''^(?:~||null|Null|NULL)$''', re.X),
            ['~', 'n', 'N', '']],
    ],
}
