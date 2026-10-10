from datetime import date
from unittest.mock import patch

from django.test import SimpleTestCase

from .models import Event


def make_event(end_date, override=Event.StatusOverride.AUTO):
    return Event(start_date=end_date, end_date=end_date, status_override=override)


@patch("django.utils.timezone.localdate", return_value=date(2026, 10, 3))
class EventStatusTests(SimpleTestCase):

    def test_not_finished_is_current(self, _):
        self.assertEqual(make_event(date(2026, 10, 3)).status, "current")
        self.assertEqual(make_event(date(2026, 12, 1)).status, "current")

    def test_ended_within_two_months_is_recent(self, _):
        self.assertEqual(make_event(date(2026, 10, 2)).status, "recent")
        self.assertEqual(make_event(date(2026, 8, 4)).status, "recent")

    def test_ended_before_two_months_is_archived(self, _):
        self.assertEqual(make_event(date(2026, 8, 3)).status, "archived")

    def test_override_wins(self, _):
        future = date(2026, 12, 1)
        old = date(2025, 1, 1)
        self.assertEqual(
            make_event(future, Event.StatusOverride.ARCHIVED).status, "archived"
        )
        self.assertEqual(make_event(old, Event.StatusOverride.RECENT).status, "recent")
