from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.page import Page
from app.models.pagerole import PageRole
from app.schemas.schema_page import PageCreate, PageRead


def crud_create_page(page_data: PageCreate, db: Session = Depends(get_db)) -> PageRead:
    new_page = Page(**page_data.dict())
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return PageRead.from_orm(new_page)


def crud_get_all_pages(db: Session = Depends(get_db)) -> list[PageRead]:
    pages = db.query(Page).order_by(Page.order_index).all()
    return [PageRead.from_orm(page) for page in pages]


def crud_get_page_by_id(page_id: UUID, db: Session = Depends(get_db)) -> PageRead:
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageRead.from_orm(page)


def crud_update_page(page_id: UUID, page_data: PageCreate, db: Session = Depends(get_db)) -> PageRead:
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    for key, value in page_data.dict().items():
        setattr(page, key, value)

    db.commit()
    db.refresh(page)
    return PageRead.from_orm(page)


def crud_delete_page(page_id: UUID, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    db.delete(page)
    db.commit()
    return {"detail": "Page deleted"}


def crud_get_pages_by_roles(role_ids: list[UUID], db: Session = Depends(get_db)) -> list[PageRead]:
    pages = db.query(Page).join(PageRole, Page.id == PageRole.page_id)
    pages = pages.filter(PageRole.role_id.in_(role_ids), Page.is_active == True).order_by(Page.order_index).all()
    return [PageRead.from_orm(page) for page in pages]
