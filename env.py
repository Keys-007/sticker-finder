#!/bin/env python
"""Commandline entry point."""
from datetime import datetime, timedelta
from stickerfinder.stickerfinder import * # noqa
from stickerfinder.models import * # noqa
from stickerfinder.db import get_session

session = get_session()


def display_reverted_changes():
    """Display all reverted changes from the last day."""
    changes = session.query(Change) \
        .filter(Change.created_at >= (datetime.now() - timedelta(days=1))) \
        .filter(Change.reverted.is_(True)) \
        .all()

    for change in changes:
        print('\nNew Tags')
        print(change.new_tags)
        print('Restored Tags')
        print(change.sticker.tags_as_text())


display_reverted_changes()