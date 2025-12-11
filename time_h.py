from datetime import datetime, timezone


# возвращает начало текущего дня, то есть 12 ночи (3 по мск)
def time_machine_param():
    timestamp = (
        datetime.now(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ).total_seconds()
    now = datetime.fromtimestamp(timestamp, timezone.utc)
    return now.strftime("%Y-%m-%dT00:00:00.000Z")


# нужно для /changes
def current_date():
    timestamp = (
        datetime.now(timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    ).total_seconds()
    now = datetime.fromtimestamp(timestamp, timezone.utc)
    return now.strftime("%d.%m.%Y 00:00")
