import datetime
import uuid

import pytz
from fastapi import HTTPException
from sqlmodel import select
from unigate.models import Join, Request

from .base_crud import CRUDBase
from .group_crud import group_crud


class CRUDRequest(CRUDBase[Request, Request, Request]):
    def get_all_requests_for_group(self, group_id: uuid.UUID) -> list[Request]:
        group = group_crud.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found.")

        return self.db_session.exec(
            select(Request).where(Request.group_id == group_id)
        ).all()

    def get_request(self, request_id: uuid.UUID) -> Request:
        request = self.db_session.exec(
            select(Request).where(Request.id == request_id)
        ).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found.")
        return request

    def approve_request(self, request_id: uuid.UUID) -> Request:
        request = self.get_request(request_id=request_id)

        if request.status == "APPROVED":
            raise HTTPException(status_code=400, detail="Request is already approved.")

        request.status = "APPROVED"
        self.db_session.add(request)

        join_entry = Join(
            student_id=request.student_id,
            group_id=request.group_id,
            date=datetime.datetime.now(tz=pytz.timezone("Europe/Rome")).date(),
        )
        self.db_session.add(join_entry)

        # Commit the transaction
        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to approve request: {e!s}"
            )

        self.db_session.refresh(request)
        return request

    def reject_request(self, request_id: uuid.UUID) -> Request:
        request = self.db_session.exec(
            select(Request).where(Request.id == request_id)
        ).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found.")

        if request.status == "REJECTED":
            raise HTTPException(status_code=400, detail="Request is already rejected.")

        request.status = "REJECTED"
        self.db_session.add(request)

        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to reject request: {e!s}"
            )

        self.db_session.refresh(request)
        return request


request_crud = CRUDRequest(Request)
