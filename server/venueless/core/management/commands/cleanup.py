import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils.timezone import now

from venueless.core.models.room import RoomView

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Perform cleanup tasks"

    def handle(self, *args, **options):
        self._cleanup_roomviews()

    def _cleanup_roomviews(self):
        # Reset RoomView objects that never "ended". In the unlikely event the session *is* still open, this will
        # *temporarily* break the statistics, but it will be auto-corrected as soon as ``end_view`` is properly
        # called.
        RoomView.objects.filter(
            end__isnull=True, start__lt=now() - timedelta(hours=6)
        ).update(end=F("start") + timedelta(hours=1))
