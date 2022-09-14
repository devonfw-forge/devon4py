import io
from datetime import datetime, timezone
from math import radians, cos, sin, asin, sqrt
from typing import BinaryIO


EARTH_RADIUS_KM = 6371.001  # Average radius of earth in kilometers. Determines return value units.


def get_current_time():
    return datetime.now(timezone.utc)


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * EARTH_RADIUS_KM


def resize_image(data: BinaryIO | bytes, size: int) -> bytes:
    from PIL import Image

    if isinstance(data, bytes):
        data = io.BytesIO(data)

    # Resize the image
    image = Image.open(data)
    image.thumbnail((size, size))

    # Create the bytes output stream and return it
    os = io.BytesIO()
    image.save(os, image.format)
    return os.getvalue()
