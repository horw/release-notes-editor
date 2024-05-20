import uvicorn
from sqlmodel import SQLModel
from db.model.merge_request import ReleaseNote
from db.session import engine
from schema.webhook.merge_request import MergeRequestWebhook
from services import release_notes_service
from fastapi import FastAPI


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def start_application():
    _app = FastAPI()
    create_db_and_tables()
    return _app


app = start_application()


@app.post("/release-notes/")
def create_release_note(release_note: ReleaseNote):
    return release_notes_service.create_release_note(release_note)


@app.get("/release-notes/")
def get_release_notes():
    return release_notes_service.get_release_notes()


@app.get("/release-notes/{mr_id}/history")
def get_release_note_history(mr_id: int):
    return release_notes_service.get_history_for_release_note(mr_id)


@app.put("/release-notes/")
def update_release_note(release_note: ReleaseNote):
    return release_notes_service.update_release_note(release_note)


@app.post("/")
def create_from_webhook(merge_webhook: MergeRequestWebhook):
    return release_notes_service.release_note_from_webhook(merge_webhook)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
