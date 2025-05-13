from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.page import Page
from app.models.pagerole import PageRole
from app.schemas.schema_page import PageCreate, PageRead
from app.core.security import require_any_permission, get_current_user

router = APIRouter()


def crud_create_page(page_data: PageCreate, db: Session = Depends(get_db)) -> PageRead:
    new_page = Page(**page_data.dict())
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return PageRead.from_orm(new_page)


@router.get("/all", response_model=list[PageRead])
def crud_get_all_pages(db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))) -> list[PageRead]:
    pages = db.query(Page).order_by(Page.order_index).all()
    return [PageRead.from_orm(page) for page in pages]


@router.get("/{page_id}", response_model=PageRead)
def crud_get_page_by_id(page_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))) -> PageRead:
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageRead.from_orm(page)


@router.put("/{page_id}", response_model=PageRead)
def crud_update_page(page_id: UUID, page_data: PageCreate, db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))) -> PageRead:
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    for key, value in page_data.dict().items():
        setattr(page, key, value)

    db.commit()
    db.refresh(page)
    return PageRead.from_orm(page)


@router.delete("/{page_id}")
def crud_delete_page(page_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    db.delete(page)
    db.commit()
    return {"detail": "Page deleted"}


@router.get("/my", response_model=list[PageRead])
def crud_get_pages_by_roles(db: Session = Depends(get_db), current_user = Depends(get_current_user)) -> list[PageRead]:
    print("CURRENT USER:", current_user)
    role_ids = current_user["role_ids"]
    print(role_ids)
    pages = db.query(Page).join(PageRole, Page.id == PageRole.page_id)
    pages = pages.filter(PageRole.role_id.in_(role_ids), Page.is_active == True).order_by(Page.order_index).all()
    return [PageRead.from_orm(page) for page in pages]


@router.post("/{page_id}/assign-role/{role_id}")
def assign_role_to_page(page_id: UUID, role_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))):
    exists = db.query(PageRole).filter_by(page_id=page_id, role_id=role_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Role already assigned to this page")
    db.add(PageRole(page_id=page_id, role_id=role_id))
    db.commit()
    return {"detail": "Role assigned to page"}


@router.delete("/{page_id}/remove-role/{role_id}")
def remove_role_from_page(page_id: UUID, role_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_any_permission("MANAGE_PAGES"))):
    assignment = db.query(PageRole).filter_by(page_id=page_id, role_id=role_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Role not assigned to this page")
    db.delete(assignment)
    db.commit()
    return {"detail": "Role removed from page"}
