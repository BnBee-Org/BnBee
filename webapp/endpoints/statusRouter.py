from fastapi import APIRouter, Depends, Response, status

router = APIRouter()


@router.get("/status")
def get_status():
    return {"status": "OK"}


@router.get("/ver")
def get_status():
    return {"version": "Alpha 0.1"}
