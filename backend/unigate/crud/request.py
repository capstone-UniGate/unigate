from unigate.models import Request
from unigate.schemas.request import RequestCreate

from .base import CRUDBase


class CRUDRequest(CRUDBase[Request, RequestCreate, Request]):
    pass


request = CRUDRequest(Request)
