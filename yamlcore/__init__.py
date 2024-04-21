import yaml
from yamlcore.loader import CommonConstructor, CommonResolver
from yamlcore.dumper import CommonRepresenter


class CommonLoader(yaml.BaseLoader, CommonConstructor, CommonResolver):

    @classmethod
    def init_tagset(cls, tagset):
        cls.init_constructors(tagset)
        cls.init_resolvers(tagset)


class CCommonLoader(yaml.CBaseLoader, CommonConstructor, CommonResolver):

    @classmethod
    def init_tagset(cls, tagset):
        cls.init_constructors(tagset)
        cls.init_resolvers(tagset)


class CoreLoader(CommonLoader):
    pass


class CCoreLoader(CCommonLoader):
    pass


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


CoreLoader.init_tagset('core')
CCoreLoader.init_tagset('core')
CoreDumper.init_tags('core')
CCoreDumper.init_tags('core')
