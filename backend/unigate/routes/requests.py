
from fastapi import APIRouter, HTTPException,Depends
from unigate.crud.request_crud import request_crud, CRUDRequest
from unigate.models import Request
from  unigate.core.database import get_session
from sqlmodel import Session, select

import uuid



router = APIRouter()

@router.post("/{request_id}/approve", response_model=Request)
def approve_group_request(request_id: uuid.UUID):

    request = request_crud.get(id=request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found or does not belong to the group.")

    approved_request = request_crud.approve_request(request_id=request_id)
    return approved_request


@router.post("/{request_id}/reject", response_model=Request)
def reject_group_request(request_id: uuid.UUID):
    request = request_crud.get(id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found or does not belong to the group.")

    rejected_request = request_crud.reject_request(request_id=request_id)
    return rejected_request