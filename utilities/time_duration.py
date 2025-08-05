from datetime import datetime as dt, timedelta

def format_timedelta(tdelta: timedelta) -> str:
    """
    Formats a datetime.timedelta object into a string with the format HH:MM:SS:MS.

    Parameters:
        tdelta (datetime.timedelta): The time duration to format.

    Returns:
        str: The formatted duration string in the format "HH:MM:SS:MS".
    """

    total_seconds = int(tdelta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    ms = int(tdelta.microseconds / 100)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}:{ms:04}"