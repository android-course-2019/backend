from .base import *


class PagingMessage(DomainBase):
    offset = DomainAttr(False, int)
    size = DomainAttr(False, int)
