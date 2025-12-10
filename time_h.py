from datetime import datetime, timezone


def sec_ago(sec):
    timestamp = (
        datetime.now(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ).total_seconds() - sec
    now = datetime.fromtimestamp(timestamp, timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
