class DomainAttr:
    def __init__(self, require: bool, attr_type: type):
        self.require = require
        self.attr_type = attr_type


class DomainBaseMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == "DomainBase":
            return type.__new__(mcs, name, bases, attrs)
        mappings = dict()
        for attr_name, attr_type in attrs.items():
            if isinstance(attr_type, DomainAttr):
                mappings[attr_name] = attr_type
        for attr in mappings.keys():
            attrs.pop(attr)
        attrs['__mappings__'] = mappings
        return type.__new__(mcs, name, bases, attrs)


class DomainBase(metaclass=DomainBaseMeta):
    def __init__(self, **kwargs):
        for k, v in self.__mappings__.items():
            if (attr := kwargs.get(k)) is not None:
                if not isinstance(attr, v.attr_type):
                    try:
                        attr = v.attr_type(attr)
                    except Exception:
                        raise TypeError
                self.__setattr__(k, attr)
            elif v.require:
                raise RequiredParamNotFoundException
            else:
                self.__setattr__(k, None)


class RequiredParamNotFoundException(BaseException):
    pass
