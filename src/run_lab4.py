import matplotlib.pyplot as plt
import json
from spatial import Parcel
from shapely.geometry import box
from spatial import SpatialObject

# Loading, Constructing, and Validating Parcels
def main():

    with open("data/parcels_shapely_ready.json", "r") as file:
        parcel_records = json.load(file)

    parcels = []

    for record in parcel_records:
        parcel = Parcel.from_dict(record)
        parcels.append(parcel)

    print(len(parcels))

    if not parcels:
        print("No parcels were loaded. Stopping script.")
        raise SystemExit

# Vector Analysis Parameters
    area_threshold = 5000.0
    min_area = 5000.0
    allowed_zones = {"Residential", "Commercial"}
    study_area = SpatialObject(
        box(121.050, 14.648, 121.060, 14.658
        ))

    # Analysis 1
    from analysis import total_active_area
    active_area = total_active_area(parcels)

    # Analysis 2
    from analysis import parcels_above_threshold
    matching_parcels = parcels_above_threshold(parcels, area_threshold)

    # Analysis 3
    from analysis import count_by_zone
    zone_counts = count_by_zone(parcels)

    # Analysis 4
    from analysis import development_candidates
    candidates = development_candidates(parcels, min_area, allowed_zones)

    # Challenge 1
    alternative_candidates = development_candidates(
        parcels, 7000.0, allowed_zones
    )
    print("Candidates with minimum area 5000:", len(candidates))
    print("Candidates with minimum area 7000:", len(alternative_candidates))

    # Analysis 5
    from analysis import intersecting_parcels
    intersect_parcel = intersecting_parcels(parcels, study_area)

    study_area_candidates = intersecting_parcels(candidates, study_area)

# Raster Analysis Functions
    from analysis import classify_suitability_grid
    from analysis import count_suitable_cells

    with open("data/suitability_grid.json", "r") as file:
        grid_data = json.load(file)

        slope_grid = grid_data["slope_deg"]
        flood_grid = grid_data["flood_m"]
        max_slope = 15.0
        max_flood = 0.5

        suitability_grid = classify_suitability_grid(
            slope_grid,
            flood_grid,
            max_slope,
            max_flood
        )

        suitable_cell_count = count_suitable_cells(suitability_grid)

        print(suitability_grid)
        print(suitable_cell_count)

    matching_parcel_ids = []
    for parcel in matching_parcels:    
        matching_parcel_ids.append(parcel.parcel_id)

    candidate_ids = []
    for parcel in candidates:
        candidate_ids.append(parcel.parcel_id)

    intersecting_parcel_ids = []
    for parcel in intersect_parcel:
        intersecting_parcel_ids.append(parcel.parcel_id)

    study_area_candidate_ids = []
    for parcel in study_area_candidates:
        study_area_candidate_ids.append(parcel.parcel_id)
    
    report = {
        "vector" : {
            "parcel_count" : len(parcels),
            "total_active_area_sqm" : active_area,
            "zone_counts" : zone_counts,
            "above_threshold_ids" : matching_parcel_ids,
            "candidate_ids" : candidate_ids,
            "study_area_candidate_ids" : study_area_candidate_ids
        },

        "raster" : {
            "rows" : len(slope_grid),
            "cols" : len(slope_grid[0]),
            "suitability_grid" : suitability_grid,
            "suitable_cell_count" : suitable_cell_count
        }
    }

# Outputs
    with open ("output/lab4_report.json", "w") as file:
        json.dump (report, file, indent=4)

    fig, ax = plt.subplots()
    for parcel in parcels:
        x, y = parcel.geometry.exterior.xy
        ax.plot(x, y)

    x, y = study_area.geometry.exterior.xy
    ax.plot(x, y, color="red", linewidth=2)

    for parcel in candidates:
        x, y = parcel.geometry.exterior.xy
        ax.fill(x, y, color="yellow")

    fig.savefig("output/lab4_vector_preview.png")
    raster_fig, raster_ax = plt.subplots()
    display_grid = []

    for row in suitability_grid:
        display_row = []
        for cell in row:
            if cell is None:
                display_row.append(-1)
            else:
                display_row.append(cell)

        display_grid.append(display_row)

    image = raster_ax.imshow(display_grid)
    raster_ax.set_title("Suitability Grid: 1 = Suitable, 0 = Unsuitable, -1 = NoData")
    raster_fig.colorbar(image, ticks=[-1, 0, 1])
    raster_fig.savefig("output/lab4_raster_preview.png")

if __name__ == "__main__":
    main()