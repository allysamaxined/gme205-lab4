#Analysis 1. total_active_area(parcels)
def total_active_area(parcels):
    total = 0.0
    for parcel in parcels:
        if parcel.is_active:
            total += parcel.area_sqm

    return total

#Analysis 2. parcels_above_threshold(parcels, threshold)
def parcels_above_threshold(parcels, threshold):
    matching_parcels = []
    for parcel in parcels:
        if parcel.area_sqm >= threshold:
            matching_parcels.append(parcel)
    return matching_parcels

#Analysis 3. count_by_zone(parcels)
def count_by_zone(parcels):
    zone_count = {}
    for parcel in parcels:
        if parcel.zone not in zone_count:
            zone_count[parcel.zone] = 0

        zone_count[parcel.zone] += 1

    return zone_count

#Analysis 4. development_candidates(parcels, min_area, allowed_zones)
def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False

    if not parcel.zone in allowed_zones:
        return False

    if parcel.area_sqm < min_area:
        return False

    return True

def development_candidates(parcels, min_area, allowed_zones):
    candidates = []
    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)
    return candidates

#Analysis 5. intersecting_parcels(parcels, study_area)
def intersecting_parcels(parcels, study_area):
    intersect_parcel = []
    for parcel in parcels:
        if parcel.intersects(study_area):
            intersect_parcel.append(parcel)
    return intersect_parcel

#Analysis 6. Raster Algorithm
def classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope,
        max_flood,
):

    if len(slope_grid) != len(flood_grid):
        raise ValueError("Slope and flood grid are not equal, must have the same number of rows.")

    for row in range(len(slope_grid)):
        if len(slope_grid[row]) != len(flood_grid[row]):
            raise ValueError("Corresponding rows must have the same number of columns!")

    suitability_grid = []

    for row in range(len(slope_grid)):
        suitability_row = []

        for col in range(len(slope_grid[row])):
            slope_value = slope_grid[row][col]
            flood_value = flood_grid[row][col]

            if slope_value is None or flood_value is None:
                classification = None

            elif slope_value <= max_slope and flood_value <= max_flood:
                classification = 1

            else:
                classification = 0

            suitability_row.append(classification)

        suitability_grid.append(suitability_row)

    return suitability_grid

def count_suitable_cells(suitability_grid):
    count = 0
    for row in suitability_grid:
        for cell in row:
            if cell == 1:
                count += 1

    return count
    