from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase
)
from app.models.song import Song
from app.schemas.song import ISongCreate
from app.schemas.song import ISongUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api import deps
from app import crud

router = APIRouter()


@router.get("/ping", response_model=IGetResponseBase)
async def pong():
    response = IGetResponseBase(data="pong!")
    return response


@router.get("/songs", response_model=IGetResponseBase[list[Song]])
async def get_songs(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db_session: AsyncSession = Depends(deps.get_db)
    ):
    songs = await crud.song.get_multi(db_session, skip=skip, limit=limit)    
    return IGetResponseBase(data=songs)


@router.post("/songs", response_model=IPostResponseBase)
async def add_song(song: ISongCreate, db_session: AsyncSession = Depends(deps.get_db)):
    new_song = await crud.song.create(db_session, obj_in=song)    
    return IPostResponseBase(data=new_song)

@router.put("/songs/{song_id}", response_model=IGetResponseBase[Song])
async def update_song(
    song_id: int,
    new_data: ISongUpdate,
    db_session: AsyncSession = Depends(deps.get_db),
):
    current_song = await crud.song.get(db_session=db_session, id=song_id)
    if not current_song:
        raise HTTPException(status_code=404, detail="Song not found")
    song_updated = await crud.song.update(
        db_session=db_session, obj_current=current_song, obj_new=new_data
    )
    return IPutResponseBase(data=song_updated)

@router.delete("/songs/{song_id}", response_model=IGetResponseBase[Song])
async def remove_team(
    song_id: int,
    db_session: AsyncSession = Depends(deps.get_db),
):
    current_song = await crud.song.get(db_session=db_session, id=song_id)
    if not current_song:
        raise HTTPException(status_code=404, detail="Song not found")
    output = await crud.song.remove(db_session, id=song_id)    
    return IDeleteResponseBase(data=output)