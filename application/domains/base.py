class DomainBase:
    @classmethod
    def __get_params(cls):
        return [i for i in cls.__dict__.items() if isinstance(i[1], DomainAttr)]

    def __init__(self, src):
        params = self.__class__.__get_params()
        for param in params:
            if param[0] not in src:
                if param[1].require:
                    raise RequiredParamNotFoundException()
            else:
                self.__setattr__(param[0], src[param[0]])


class DomainAttr:
    def __init__(self, require: bool, attr_type: type):
        self.require = require
        self.attr_type = attr_type


class RequiredParamNotFoundException(BaseException):
    pass
