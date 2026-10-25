import yaml
from yamlcore.loader import CommonConstructor, CommonResolver
from yamlcore.dumper import CommonRepresenter


class CommonLoader(yaml.BaseLoader, CommonConstructor, CommonResolver):

    @classmethod
    def init_tagset(cls, tagset):
        cls.init_constructors(tagset)
        cls.init_resolvers(tagset)


if yaml.__with_libyaml__:

    class CCommonLoader(yaml.CBaseLoader, CommonConstructor, CommonResolver):

        @classmethod
        def init_tagset(cls, tagset):
            cls.init_constructors(tagset)
            cls.init_resolvers(tagset)


    class CCoreLoader(CCommonLoader):
        pass


class CoreLoader(CommonLoader):
    pass


class CommonDumper(yaml.BaseDumper, CommonRepresenter, CommonResolver):

    @classmethod
    def init_tags(cls, tagset):
        cls.init_representers(tagset)
        cls.init_resolvers(tagset)


if yaml.__with_libyaml__:

    class CCommonDumper(yaml.CBaseDumper, CommonRepresenter, CommonResolver):

        @classmethod
        def init_tags(cls, tagset):
            cls.init_representers(tagset)
            cls.init_resolvers(tagset)


    class CCoreDumper(CCommonDumper):
        pass


class CoreDumper(CommonDumper):
    pass


CoreLoader.init_tagset('core')
CoreDumper.init_tags('core')
if yaml.__with_libyaml__:
    CCoreLoader.init_tagset('core')
    CCoreDumper.init_tags('core')
