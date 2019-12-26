from .base import DomainBase, DomainAttr


class LoginParam(DomainBase):
    phone = DomainAttr(True, str)
    password = DomainAttr(True, str)


class SignUpParam(DomainBase):
    phone = DomainAttr(True, str)
    password = DomainAttr(True, str)
    validateCode = DomainAttr(True, str)
    nickName = DomainAttr(True, str)


class SendSmsParam(DomainBase):
    phone = DomainAttr(True, str)
    checkExist = DomainAttr(False, bool)
