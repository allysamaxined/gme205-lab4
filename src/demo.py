# Test/Demonstration of Analysis 1. total_active_area
from spatial import Parcel
from analysis import total_active_area
from shapely.geometry import Polygon
import json

polygon = Polygon ([
    (0,0),
    (1,0),
    (1,1),
    (0,1)
])

outside_polygon = Polygon ([
    (3, 3),
    (4, 3),
    (4, 4),
    (3, 4)
])

p1 = Parcel(1, polygon, attributes = {
    "area_sqm" : 100.0,
    "is_active" : True,
    "zone" : 'Residential'
})

p2 = Parcel(2, polygon, attributes = {
    "area_sqm" : 200.0,
    "is_active" : False,
    "zone" : "Residential"
})

p3 = Parcel(3, polygon, attributes = {
    "area_sqm" : 300.0,
    "is_active" : True,
    "zone" : "Industrial"
})

p4 = Parcel(4, polygon, attributes = {
    "area_sqm" : 6000,
    "is_active" : False,
    "zone" : "Residential"
})

p5 = Parcel(5, polygon, attributes = {
    "area_sqm" : 6000,
    "is_active" : True,
    "zone" : "Industrial"
})

p6 = Parcel(6, polygon, attributes = {
    "area_sqm" : 4000,
    "is_active" : True,
    "zone" : "Commercial"
})

p7 = Parcel(7, polygon, attributes = {
    "area_sqm" : 5000,
    "is_active" : True,
    "zone" : "Residential"
})

p8 = Parcel(8, outside_polygon, attributes = {
    "area_sqm" : 8000,
    "is_active" : True,
    "zone" : "Residential"
})

parcels = [p1, p2, p3]
result = total_active_area(parcels)
print(result)

#Test/Demonstration for Analysis 2. parcels_above_threshold
from analysis import parcels_above_threshold

matches = parcels_above_threshold(parcels, 200.0)
for parcel in matches:
    print(parcel.parcel_id)

#Test/Demonstration for Analysis 3. count_by_zone(parcels)
from analysis import count_by_zone

zone_counts = count_by_zone(parcels)
print(zone_counts)

#Test/Demonstration for Analysis 4. is_development_candidate
from analysis import development_candidates

candidate_samples = [p4, p5, p6, p7]
allowed_zones = {"Residential", "Commercial"}
candidates = development_candidates(candidate_samples, 5000, allowed_zones)
for parcel in candidates:
    print(parcel.parcel_id)

#Test/Demonstration for Analysis 5. intersecting_parcels
from analysis import intersecting_parcels
from spatial import SpatialObject

study_area = SpatialObject(polygon)
intersection_sample = [p1, p8]
intersections = intersecting_parcels(intersection_sample, study_area)
for parcel in intersections:
    print(parcel.parcel_id)

#Test/Demonstration of Analysis 6. Raster Algorithm
from analysis import classify_suitability_grid

slope_sample = [
    [10, 20],
    [None, 15]
]

flood_sample = [
    [0.3, 0.2],
    [0.1, 0.5]
]

classified_suitability_grid = classify_suitability_grid(slope_sample, flood_sample, max_slope=15.0, max_flood=0.5)
print(classified_suitability_grid)

from analysis import count_suitable_cells

suitable_cells = count_suitable_cells(classified_suitability_grid)
print(suitable_cells)

slope_check = [[10, 10]]
flood_check = [[0.8, None]]

suitability_check = classify_suitability_grid(
    slope_check, 
    flood_check,
    max_slope=15.0,
    max_flood=0.5
)
print(suitability_check)
check_count = count_suitable_cells(suitability_check)
print(check_count)