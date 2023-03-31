
import datetime

def convert_utc_to_cvt(utc_timestamp):
    from datetime import datetime, timedelta

    # Convert UTC timestamp to datetime object
    dt_utc = datetime.fromisoformat(utc_timestamp[:-1])

    # Calculate the time difference between CVT and UTC
    cvt_offset = timedelta(hours=-1)  # Standard Time

    # Convert UTC datetime object to CVT datetime object
    dt_cvt = dt_utc + cvt_offset

    # Format the CVT datetime object as a string
    cvt_timestamp = dt_cvt.isoformat() + 'Z'

    return cvt_timestamp




