import math
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import shape

# Creating the SpatialObject here.

class SpatialObject:
    """Base abstraction for domain objects that have geometry."""

    def __init__(self, geometry):
        self.geometry = geometry

    def bbox (self):
        return self.geometry.bounds

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

# Turning Point to a class that inherits from SpatialObject.

class Point(SpatialObject):
    def __init__(self, id, lon, lat, name=None, tag=None):

        # This will be used to validate longitude and latitude.
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90.")

        geometry = ShapelyPoint(lon, lat)
        super().__init__(geometry)
        self.id = id
        self.name = name
        self.tag = tag

# Preserving the access to Longitude and Latitude using Properties.
    @property
    def lon(self):
        return self.geometry.x

    @property
    def lat(self):
        return self.geometry.y
    
# ------------------------------------------------------------------ 
# Instance methods (behavior belongs to the object)
# ------------------------------------------------------------------

    def to_tuple (self) -> tuple [float, float]:
        """
        Return the coordinate as a (lon, lat) tuple.
        """
        return (self.lon, self.lat)
    def distance_to (self, other):
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)

# ------------------------------------------------------------------ 
# Static method (pure spatial math)
# ------------------------------------------------------------------
    @staticmethod
    def haversine_m (
        lon1: float, lat1: float, lon2: float, lat2: float
        ) -> float:
        """
        Compute the Haversine distance between two lon/lat pairs in meters.
        
        Static method because it does not depend on object state.
        """
        R = 6_371_000 # Earth's radius in meters

        phi1 = math.radians (lat1)
        phi2 = math.radians (lat2)
        dphi = math.radians (lat2 - lat1)
        dlambda = math.radians (lon2 - lon1)

        a = (
            math.sin (dphi / 2) ** 2
            + math.cos (phi1)
            * math.cos (phi2)
            * math.sin (dlambda / 2) ** 2
        )

        c = 2 * math.atan2 (math.sqrt(a), math.sqrt(1 - a))
        return R * c

# ------------------------------------------------------------------ 
# Class method (constructing objects from data)
# ------------------------------------------------------------------
    @classmethod
    def from_row (cls, row):
        return cls (
            id = str(row ["id"]),
            lon = float(row ["lon"]),
            lat = float(row ["lat"]),
            name = row.get ("name"),
            tag = row.get ("tag"),
        )

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"],
            d["lon"],
            d["lat"],
            d.get("name"),
            d.get("tag")
        )

    def as_dict(self):
        return {
            "id" : self.id,
            "geometry" : [self.lon, self.lat],
            "name" : self.name,
            "tag" : self.tag,
            "bbox": list(self.bbox())
        }

    def is_poi (self):
        return (self.tag or "").lower() == "poi"

# Adding the Parcel class.
class Parcel(SpatialObject):
    def __init__(self, parcel_id, geometry, attributes: dict):
        super().__init__(geometry)
        self.parcel_id = parcel_id
        self.attributes = attributes

# Implementing Parcel.as_dict()
    def as_dict(self):
        return {
            "parcel_id" : self.parcel_id,
            "bbox" : list(self.bbox()),
            "attributes" : self.attributes
        }

    @property
    def area_sqm(self):
        return float(self.attributes["area_sqm"])

    @property
    def zone(self):
        return self.attributes["zone"]

    @property
    def is_active(self):
        return bool(self.attributes["is_active"])
    
    @classmethod
    def from_dict(cls, record):
        geometry = shape(record["geometry"])
        attributes = {
            "zone" : record["zone"],
            "is_active" : record["is_active"],
            "area_sqm" : record["area_sqm"]
        }
        return cls(record["parcel_id"], geometry, attributes)