from datetime import datetime
from zoneinfo import ZoneInfo

from django.shortcuts import render

from corpus.decorators import event_time_gate


def home(request):
    return render(request, "tlm/home.html")


tz = ZoneInfo("Asia/Kolkata")

launch_time = datetime(2026, 3, 20, 18, 0, 0, tzinfo=tz)
end_time = datetime(2026, 3, 24, 18, 0, 0, tzinfo=tz)


@event_time_gate(
    start_time=launch_time,
    end_time=end_time,
    pre_template="tlm/403.html",
    post_template="tlm/403_end.html",
    context={"message": "Event access restricted"},
)
def landing(request):
    context = {
        "countdown_target": int(end_time.timestamp() * 1000),
    }
    return render(request, "tlm/landing.html", context)
