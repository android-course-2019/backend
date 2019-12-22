from .base import DomainBase, DomainAttr


class GetPosterParam(DomainBase):
    offset = DomainAttr(False, int)
    size = DomainAttr(False, int)


class CreatePosterParam(DomainBase):
    brandName = DomainAttr(False, str)
    shopId = DomainAttr(False, int)
    shopName = DomainAttr(False, str)
    drinks = DomainAttr(True, int)
    content = DomainAttr(True, str)
    images = DomainAttr(False, list)
