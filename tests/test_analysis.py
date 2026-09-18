from src.spatial import Parcel
from src.analysis import total_active_area
from shapely.geometry import Polygon
from src.analysis import parcels_above_threshold
from src.analysis import count_by_zone
from src.analysis import development_candidates
from src.analysis import intersecting_parcels
from src.spatial import SpatialObject
from src.analysis import classify_suitability_grid
from src.analysis import count_suitable_cells

# Total Active Area
polygon = Polygon ([
    (0,0),
    (1,0),
    (1,1),
    (0,1)
])

def test_total_active_area():
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

    parcels = [p1, p2]
    result = total_active_area(parcels)
    print(result)
test_total_active_area()

# Parcels Above Threshold

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

def test_parcels_above_threshold():
    parcels = [p1, p2, p3]
    matches = parcels_above_threshold(parcels, 200.0)
    for parcels in matches:
        print(parcels.parcel_id)
test_parcels_above_threshold()

# Count by Zone

def test_zone_counts():
    parcels = [p1, p2, p3]
    zone_counts = count_by_zone(parcels)
    print(zone_counts)
    print(sum(zone_counts.values()) == len(parcels))
test_zone_counts()

# Development Candidates

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

def test_development_candidates():
    candidate_samples = [p4, p5, p6, p7]
    allowed_zones = {"Residential", "Commercial"}
    candidates = development_candidates(candidate_samples, 5000, allowed_zones)
    for parcel in candidates:
        print(parcel.parcel_id)
        print(parcel.is_active)
        print(parcel.zone in allowed_zones)
        print(parcel.area_sqm >= 5000.0)

    study_area = SpatialObject(polygon)
    study_area_candidates = intersecting_parcels(candidates, study_area)
    for parcel in study_area_candidates:
        print(parcel in candidates)

test_development_candidates()

# Intersecting Parcels

outside_polygon = Polygon ([
    (3, 3),
    (4, 3),
    (4, 4),
    (3, 4)
])

p8 = Parcel(8, outside_polygon, attributes = {
    "area_sqm" : 8000,
    "is_active" : True,
    "zone" : "Residential"
})

def test_intersecting_parcels():
    study_area = SpatialObject(polygon)
    intersection_sample = [p1, p8]
    intersections = intersecting_parcels(intersection_sample, study_area)
    for parcel in intersections:
        print(parcel.parcel_id)
test_intersecting_parcels()

# Raster Sets

slope_sample = [
    [10, 20],
    [None, 15]
]

flood_sample = [
    [0.3, 0.2],
    [0.1, 0.5]
]

def test_classify_suitability_grid():
    classified_suitability_grid = classify_suitability_grid(
        slope_sample, flood_sample, max_slope=15.0, max_flood=0.5)
    print(classified_suitability_grid)
    print(len(classified_suitability_grid) == len(slope_sample))
    for row in range(len(slope_sample)):
        print(len(classified_suitability_grid[row]) == len(slope_sample[row]))

def test_count_suitable_cells():
    classified_grid = classify_suitability_grid(
        slope_sample, flood_sample, max_slope=15.0, max_flood=0.5)
    suitable_cells = count_suitable_cells(classified_grid)
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
test_count_suitable_cells()
test_classify_suitability_grid()

# Testing Mismatch
def test_grid_dimension_mismatch():
    max_slope = 15.0
    max_flood = 0.5

    slope_check = [[10, 15]]
    flood_check = [[0.3]]

    try:
        classify_suitability_grid(slope_check, flood_check, max_slope, max_flood)
    except ValueError:
        print("The expected ValueError was caught.")

    slope_check = [[10], [15]]
    flood_check = [[0.3]]

    try:
        classify_suitability_grid(slope_check, flood_check, max_slope, max_flood)
    except ValueError:
        print("Unequal rows found!")
    
test_grid_dimension_mismatch()