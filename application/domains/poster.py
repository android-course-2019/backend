from .base import DomainBase, DomainAttr


class GetPosterParam(DomainBase):
    offset = DomainAttr(False, int)
    size = DomainAttr(False, int)
