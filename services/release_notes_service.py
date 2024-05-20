import requests

from faker import Faker
from configuration import settings
from db.model.merge_request import ReleaseNote, History
from db.session import engine
from sqlmodel import Session, select


def create_release_note(release_note):
    with Session(engine) as session:
        session.add(release_note)
        session.commit()
        session.refresh(release_note)
        return release_note


def get_release_notes():
    with Session(engine) as session:
        release_notes = session.exec(select(ReleaseNote)).all()
        return release_notes


def get_history_for_release_note(mr_id):
    with Session(engine) as session:
        history = session.exec(select(History).where(History.mr_id == mr_id)).all()
        return history


def update_release_note(release_note):
    with Session(engine) as session:
        prev_release_note = session.exec(
            select(ReleaseNote).where(ReleaseNote.id == release_note.id)
        ).first()
        if not prev_release_note:
            return

        description_was_changed = prev_release_note.current_description != release_note.current_description
        if not description_was_changed:
            return

        prev_release_note.current_description = release_note.current_description
        history = History(
            description=release_note.current_description,
            mr_id=release_note.id
        )
        session.add(history)
        session.commit()


def release_note_from_webhook(merge_webhook):
    with Session(engine) as session:
        description_was_changed = True

        prev_release_note = session.exec(
            select(ReleaseNote).where(ReleaseNote.url == merge_webhook.object_attributes.url)
        ).first()
        if prev_release_note:
            description_was_changed = prev_release_note.current_description != merge_webhook.object_attributes.description
            prev_release_note.current_description = merge_webhook.object_attributes.description
            release_note = prev_release_note
        else:
            release_note = ReleaseNote(
                current_description=merge_webhook.object_attributes.description,
                url=merge_webhook.object_attributes.url
            )
            session.add(release_note)
        session.commit()

        if description_was_changed:
            history = History(
                description=merge_webhook.object_attributes.description,
                mr_id=release_note.id
            )
            session.add(history)
            session.commit()

        if not merge_webhook.object_attributes.description.startswith('[U]'):
            fake = Faker()
            paragraph = fake.paragraph()
            headers = {'PRIVATE-TOKEN': settings.GIT_TOKEN}
            response = requests.put(
                f'https://{settings.GIT_DOMAIN}/api/v4/projects/{merge_webhook.project.id}/merge_requests/{merge_webhook.object_attributes.iid}',
                headers=headers,
                json={"description": f"[U][1]{paragraph}"}
            )

        return release_note
