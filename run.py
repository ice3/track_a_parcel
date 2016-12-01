#!/usr/bin/env python
"""Run the app."""

from app import app
from app.utils import update_events_periodically


SECONDS_PER_HOUR = 3600
update_events_periodically(SECONDS_PER_HOUR * 5)

app.run(debug=True)
