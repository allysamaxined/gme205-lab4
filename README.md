# Programming Exercise 4
## Spatial Algorithms and Structured Programming

#### Vector Analysis Algorithm (*PSEUDOCODE*)

##### Input and Output
The input must load the data needed for the project and ensure that the required parameters to run it is available or in place.

Vector Analysis Inputs
- parcel records
- area threshold
- allowed zones
- development candidates minimum area
- study area

Vector Analysis Outputs
- total_active_area
- acceptable_parcels
- zones
- development_candidates
- intersecting_parcels

Raster Analysis Inputs
- slope_grid
- flood_grid
- slope_criteria
- flood_m_criteria

Raster Analysis Outputs
- suitability_grid 
- suitable_cell_count

The output must describe or show the results produced by running the project.

Therefore, the overall sequence must be:
1. Load data: parcel records and raster grids.
2. Prepare and verify inputs: construct Parcel objects using Parcel.from_dict(); stop/report if none are loaded; verify matching raster dimensions.
3. Analyze: perform the five vector analyses and classify the raster grid.
4. Count: count raster cells classified as 1.
5. Report: assemble results and produce outputs.

##### Control Structures
- Sequence: Load data -> prepare and verify inputs -> analyze -> count suitable cells -> produce the report.
- Selection: Check parcel activity, area thresholds, allowed zones, and intersections. For raster cells, check NoData or NULL and both suitability criteria.
- Repetition: Loop through parcels for vector analysis. Use nested row-and-column loops for raster classification and counting.

###### Analysis for Q1.  What is the total area in square meters of all active parcels?
```
total_active_area = 0

FOR each parcel in parcels
    IF parcel is active
        ADD parcel area_sqm to total_active_area
    END IF
END FOR
RETURN total_active_area
```

###### Analysis for Q2.  Which parcels have area greater than or equal to a chosen threshold?
```
acceptable_parcels = [empty list, for storage purposes]

FOR each parcel in parcels
    IF parcel.area_sqm >= threshold value
        ADD parcel to acceptable_parcels
    END IF
END FOR
RETURN acceptable_parcels
```

###### Analysis for Q3.  How many parcels belong to each zone?
```
zones = {empty dictionary, for storage purposes}

FOR each parcel in parcels
    IF parcel.zone not yet in zones
        SET zones[parcel.zone] = 0
    END IF

    ADD 1 to zones[parcel.zone]
END FOR
RETURN zones
```

###### Analysis for Q4. Which parcels are development candidates under this rule: active, zone is Residential or Commercial, and area is at least 5,000 m²?
```
allowed_zones = {'Residential', 'Commercial'}
min_area = 5000

DEF is_development_candidate(parcel, min_area, allowed_zones)
    IF parcel is not active
        RETURN False
    END IF

    IF parcel.zone is not in allowed_zones
        RETURN False
    END IF 

    IF parcel.area_sqm is below min_area
        RETURN False
    END IF        

    RETURN TRUE
END DEF

DEF development_candidates(parcels, min_area, allowed_zones)
    CREATE candidates as an empty list
    FOR parcel in parcels
        IF is_development_candidate(parcel, min_area, allowed_zones)
            ADD parcel to candidates
        END IF
        
    END FOR
    RETURN candidates

END DEF
```

##### Analysis for Q5. Which parcels intersect a defined study-area polygon?
```
intersecting_parcels = [empty list, for storage purposes]
defined_area = study area polygon

FOR each parcel in parcels
    IF parcel.intersects(defined_area)
        ADD parcel to intersecting_parcels

    END IF
END FOR
RETURN intersecting_parcels
```

#### Raster Analysis Algorithm (*PSEUDOCODE*)

##### Analysis for Q6. Using a small raster-style grid, which cells satisfy both slope and flood criteria?
```
READ slope_grid from suitability_grid.json
READ flood_grid from suitability_grid.json
READ slope_criteria and flood_m_criteria from suitability_grid.json

VERIFY both grids have matching row and col dimensions
IF dimensions do not match
    REPORT dimension error and STOP
END IF

SET rows and cols from verified grid dimensions 

CREATE an empty suitability_grid
SET suitable_cell_count to 0
        
FOR row in range(rows)
    CREATE output_row (empty row)

    FOR col in range(cols)
        READ slope_value = slope_grid[row][col]
        READ flood_value = flood_grid[row][col]

        IF either value is NULL
            SET result to NULL

        ELIF  slope_value <= slope_criteria AND flood_value <= flood_m_criteria
            SET result to 1

        ELSE
            SET result to 0

        END IF

        ADD result to output_row

    END FOR
        
    ADD output_row to suitability_grid

END FOR

FOR each row in suitability_grid
    FOR each result in row
        IF result = 1
            ADD 1 to suitable_cell_count
        END IF
    END FOR
END FOR    

RETURN suitability_grid and suitable_cell_count
```