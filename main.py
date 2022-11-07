from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

import schemas, models
from database import Base, engine, SessionLocal


Base.metadata.create_all(engine)

def get_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()



app=FastAPI()


@app.get("/")
async def get_items(session:Session=Depends(get_session)):
    items=session.query(models.Item).all()
    return items


@app.get("/{id}")
async def get_item(id:int,session:Session=Depends(get_session)):
    item= session.query(models.Item).filter(models.Item.id==id).first()
    return item

@app.post("/", status_code=status.HTTP_201_CREATED)
async def add_item(item:schemas.Item, session:Session=Depends(get_session)):
    item=models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item 

@app.put("/{id}")
async def update_item(id:int, updatedItem:schemas.Item, session:Session=Depends(get_session)):
    item=session.query(models.Item).filter(models.Item.id==id).first()
    item.task=updatedItem.task
    session.commit()
    return item 



@app.delete("/{id}")
async def delete_item(id:int, session: Session=Depends(get_session)):
    item=session.query(models.Item).filter(models.Item.id==id).first()
    session.delete(item)
    session.commit()
    return {f"item with  ID={id} IS DELETED "}