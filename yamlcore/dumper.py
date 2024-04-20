import yaml
from yamlcore.loader import CommonResolver


class CommonRepresenter(yaml.representer.BaseRepresenter):

    inf_value = 1e300
    while repr(inf_value) != repr(inf_value*inf_value):
        inf_value *= inf_value

    @classmethod
    def init_representers(cls, name):
        for key in _representers[name]:
            callback = _representers[name][key]
            cls.add_representer(key, callback)

    def ignore_aliases(self, data):
        if data is None:
            return True
        if isinstance(data, tuple) and data == ():
            return True
        if isinstance(data, (str, bytes, bool, int, float)):
            return True


class CommonDumper(yaml.BaseDumper, CommonRepresenter, CommonResolver):

    @classmethod
    def init_tags(cls, tagset):
        cls.init_representers(tagset)
        cls.init_resolvers(tagset)


class CCommonDumper(yaml.CBaseDumper, CommonRepresenter, CommonResolver):

    @classmethod
    def init_tags(cls, tagset):
        cls.init_representers(tagset)
        cls.init_resolvers(tagset)


class CoreDumper(CommonDumper):
    pass


class CCoreDumper(CCommonDumper):
    pass


class CommonRepresenter(yaml.representer.BaseRepresenter):

    inf_value = 1e300
    while repr(inf_value) != repr(inf_value*inf_value):
        inf_value *= inf_value

    @classmethod
    def init_representers(cls, name):
        for key in _representers[name]:
            callback = _representers[name][key]
            cls.add_representer(key, callback)

    def ignore_aliases(self, data):
        if data is None:
            return True
        if isinstance(data, tuple) and data == ():
            return True
        if isinstance(data, (str, bytes, bool, int, float)):
            return True


_representers = {
    'core': {
        bool: yaml.representer.SafeRepresenter.represent_bool,
        dict: yaml.representer.SafeRepresenter.represent_dict,
        list: yaml.representer.SafeRepresenter.represent_list,
        tuple: yaml.representer.SafeRepresenter.represent_list,
        str: yaml.representer.SafeRepresenter.represent_str,
        float: yaml.representer.SafeRepresenter.represent_float,
        int: yaml.representer.SafeRepresenter.represent_int,
        type(None): yaml.representer.SafeRepresenter.represent_none,
        None: yaml.representer.SafeRepresenter.represent_undefined,
    },
}

CoreDumper.init_tags('core')
CCoreDumper.init_tags('core')
