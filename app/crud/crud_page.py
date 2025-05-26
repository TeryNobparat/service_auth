from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.page import Page
from app.models.pagerole import PageRole
from app.schemas.schema_page import PageCreate, PageRead,RolePageUpdate


from collections import defaultdict
from app.schemas.schema_page import PageRead

def build_page_tree(pages: list[Page]) -> list[PageRead]:
    page_map = {str(p.id): PageRead.from_orm(p) for p in pages}
    tree = []

    for page in page_map.values():
        page.children = []  # reset ก่อน
    for p in pages:
        if p.parent_id is not None:
            parent_id = str(p.parent_id)
            if parent_id in page_map:
                page_map[parent_id].children.append(page_map[str(p.id)]) # type: ignore
        else:
            tree.append(page_map[str(p.id)])

    return tree


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

def crud_update_is_active(page_id: UUID, is_active: bool, db: Session = Depends(get_db)) -> PageRead:
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    page.is_active = is_active  # type: ignore
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



def crud_post_page_roles(page_id: UUID, role_ids: list[UUID], db: Session = Depends(get_db)):
    print("ROLE IDS:", role_ids)
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    db.query(PageRole).filter(PageRole.page_id == page_id).delete()

    for role_id in role_ids:
        new_page_role = PageRole(page_id=page_id, role_id=role_id)
        db.add(new_page_role)

    db.commit()
    return {"detail": "Page roles updated"}


