from src.spatial import Parcel

# Parcel Properties
def parcel_properties():
    record = {
        "parcel_id" : 1,
        "zone" : "Residential",
        "is_active" : True,
        "area_sqm" : 5000.0,
        "geometry" : {
            "type" : "Polygon",
            "coordinates" : [[
                [0,0],
                [1,0],
                [1,1],
                [0,1],
                [0,0]
            ]]
        }
    }

    parcel = Parcel.from_dict(record)
    print(parcel.parcel_id)
    print(parcel.zone)
    print(parcel.is_active)
    print(parcel.area_sqm)
    print(parcel.geometry.geom_type)
parcel_properties()