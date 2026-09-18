# Programming Exercise 4
## Spatial Algorithms and Structured Programming

#### Introduction to the Programming Exercise
This programming exercise will turn the familiair GIS analysis into explicit algorithms using sequence, selection, repetition, functions, and clean object responsibilities. We already know GIS operations and tools, and this laboratory helps us see the computational logic behind it visibly. For each of those tool, there is a program that runs on the backend.

### Materials/Requirements
1. Python
2. VS Code
3. Git/GitHub
4. Shapely
5. JSON
6. matplotlib

### Python Libraries Used
1. matplotlib
2. Shapely
3. json

### Project Structure
The structure of this project is as follows:
```
gme205-lab4/
├── .venv/
├── data/
│   ├── parcels_shapely_ready.json
│   └── suitability_grid.json
├── output/
│   ├── lab4_report.json
│   ├── lab4_vector_preview.png
│   └── lab4_raster_preview.png
├── src/
│   ├── spatial.py
│   ├── analysis.py
│   ├── demo.py
│   └── run_lab4.py
├── tests/
│   ├── test_spatial.py
│   └── test_analysis.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Environment Setup
1. Create the root directory.
2. Open VS Code > root folder > create the virtual environment.
```
python -m venv .venv
```
3. Activate the venv using:
```
.\.venv\Scripts\activate
```
4. Select Python Interpreter and install required dependencies.
```
pip install --upgrade pip
pip install matplotlib shapely
pip install -r requirements.txt
pip freeze > requirements.txt
```
5. (.venv) Must be activated, commands must be executed in the root directory.

### Running the Program
To run the demonstration, call Python and run `src/demo.py`
To run the complete workflow, call Python and run `src/run_lab4.py`
To run the focused tests, and run `python -m tests.test_analysis` or `python -m tests.test_spatial`

#### Algorithm and Pseudocode
### Vector Analysis Algorithm (*PSEUDOCODE*)

### Input and Output
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

### Control Structures
- Sequence: Load data -> prepare and verify inputs -> analyze -> count suitable cells -> produce the report.
- Selection: Check parcel activity, area thresholds, allowed zones, and intersections. For raster cells, check NoData or NULL and both suitability criteria.
- Repetition: Loop through parcels for vector analysis. Use nested row-and-column loops for raster classification and counting.

### Analysis for Q1.  What is the total area in square meters of all active parcels?
```
total_active_area = 0

FOR each parcel in parcels
    IF parcel is active
        ADD parcel area_sqm to total_active_area
    END IF
END FOR
RETURN total_active_area
```

### Analysis for Q2.  Which parcels have area greater than or equal to a chosen threshold?
```
acceptable_parcels = [empty list, for storage purposes]

FOR each parcel in parcels
    IF parcel.area_sqm >= threshold value
        ADD parcel to acceptable_parcels
    END IF
END FOR
RETURN acceptable_parcels
```

### Analysis for Q3.  How many parcels belong to each zone?
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

### Analysis for Q4. Which parcels are development candidates under this rule: active, zone is Residential or Commercial, and area is at least 5,000 m²?
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

### Analysis for Q5. Which parcels intersect a defined study-area polygon?
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

### Raster Analysis Algorithm (*PSEUDOCODE*)

### Analysis for Q6. Using a small raster-style grid, which cells satisfy both slope and flood criteria?
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
#### Results and Outputs
To view output, open output folder and view:
1. lab4_raster_preview.png
2. lab4_vector_preview.png
3. lab4_report.json

#### Required Challenges
### Challenge 1: Changing the Policy
In Challenge 1, I used the same function and tasked it to select twice with different minimum areas. This was demonstrated in `run_lab4.py`. Both produced results, for `candidates`, there were 45 candidates that were at least 5000 sqm., and 34 with at least 7000 sqm. for the second candidate. 

This did not change the algorithm, or it did not require me to write it again. I was able to change just the policy while being confident that the same function runs.

### Challenge 2: Compose, Do Not Duplicate
With `candidates`, I was able to find eligible development parcels. I then, passed that list to `intersecting_parcels`. This way, I was able to keep just those that intersect the study area.

I combined two existing functions rather than copying the same checks into the intersection function. Both functions performed as individual functions and produced the results.

### Challenge 3. Refractor Explanation
In determining the candidates or development parcels, I separated two functions. First, I set the `is_development_candidate` to check whether one parcel is qualified by using early returns. Then, I used `development_candidates()` to loop through parcels, and collect those who are candidates, those who qualified.

For this Lab Ex, I spent a lot of time trying to make the code that mirrors the guide provided, the document showing the Good and Bad algorithms. As much as I could, I followed that and prevented nesting. I did have a lot of challenge writing the syntax, but I made sure to refrain from nesting. In this case, I won't have examples of the duplication. The final code I used was this (from src/analysis.py):
```
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
```

### Challenge 4. Vector and Raster Comparison
Vector analysis loops through Parcel objects in a list, using their properties and spatial behavior. Raster analysis uses nested loops through rows and columns, accessing individual cell values by their indices. These details depend on how the data is represented.

Both approaches use sequence to organize the workflow, selection to check criteria, and repetition to process the data. Separate analysis functions keep tasks modular and reusable. The vector object model additionally uses OOP to organize parcel state and shared geometry behavior.

#### Reflection Questions
### 1. Algorithm: Choose one vector-analysis question. How did writing the algorithm/pseudocode first change the way you implemented it?
In Question 1, by writing the pseudocode first, I had the idea of how to write the proper syntax for the actual runner. I already had the thinking and preparation as to the libraries that will need to be called, and how it could potentially look like. I personally find it challenging to do syntax, but with pseudocoding, that improved. 

The most notable change was that, I knew how to structure it in the actual program. I knew where to begin, and what to write to follow through. I had a guide and I used to determine how to proceed with the script.

### 2. Control flow: Where do sequence, selection, and repetition explicitly appear in your final system?
**Sequence** can be observed in `run_lab4.py`. It loads the data, constructs the parcels, runs the analyses, and then, saves the output. The sequence of tasks are clear here.

**Selection** is seen or is applied in different functions, but a specific example is the `is_development_candidate` function. This checked eligibility of a parcel's activity, zone, and area. Additionally, `classify_suitability_grid` checked a cell's NoData status, slope, and flood values.

**Repetition** is seen throughout the script. There are a lot of loops included, properly structured (and not nested unnecessarily). One example is how the vector functions loop through the parcels, and how the raster functions loop through the rows and columns.


### 3. Responsibility: Give one behavior that belongs to Parcel/SpatialObject and one rule that belongs to analysis.py. Why? 
The spatial behavior retained in `Parcel/SpatialObject` is `intersects()`, because it operates on an object's geometry. On the other hand, `analysis.py` owns the development eligibility rules, checking whether parcels are active, belong to allowed zones, and meet the minimum area.

These eligibility rules are changeable project policies, while spatial intersection is reusable geometry behavior. Keeping them separate allows the policy to change without modifying the spatial classes.

### 4. Conditional structure: What specific design choice prevents your development-candidate logic from becoming nested conditional chaos?
To prevent the logic from being chaotically nested, I used a *helper* that checks each parcel’s eligibility through separate conditions and returns `False` as soon as one fails. If all conditions pass, it returns `True`. This avoids deeply nested conditions and keeps the collection loop separate from the eligibility rules.

### 5. Area meaning: Why does this exercise use area_sqm instead of interpreting geometry.area as square meters?
The `area_sqm` values from `parcels_shapely_ready.json` appear in square meters as its measurement units per object. I used `area_sqm` because it provides parcel area in that unit. The geometry uses longitude/latitude coordinates, so `geometry.area` cannot be interpreted directly as square meters.

### 6. Vector vs raster: How is repetition different when processing Parcel objects versus a 2D raster-style grid? What remains conceptually the same?
The difference is that, the vector functions loop through each Parcel object, while raster functions use nested loops through rows and columns. Both repeatedly check criteria and collect or count results; the data representation differs, but the repetition follows the same basic idea.

### 7. Scale: If the input grew to one million parcels or a 10,000 × 10,000 raster, which parts of this design remain useful and which implementation choices would need to change?
The functions would remain useful, as well as the analyses checks in src/analysis.py and the tests/test_analysis.py. However, the runner script might find challenges along the way due to the amount of data it has to load, process, analyze, and produce an output for. At that scale, I would need to process data in batches or grid blocks rather than loading everything at once, and limit what gets plotted. The responsibility boundaries could stay the same, while the loading and processing methods would need to change.