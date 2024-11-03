# Junior Backend Developer Take-Home Assignment Berezovskii

Hello! This is the solution for the Junior Backend Developer Take-Home Assignment
submitted by Stanislav Berezovskii for refinq GmbH.

Getting Started

    Clone this repository to your computer and navigate to the project locally.
    Ensure you have Python 3.10+ installed.
    Create and activate virtual environment.
    Install dependencies using pip install -r requirements.txt.
    Run python -m alembic upgrade head to set up the database.
    Run the FastAPI server using python -m uvicorn app.main:app --reload.
    Open http://localhost:8000/docs in your browser to see the API documentation and to test it.
    For running tests use python -m pytest.
    (Use command python tests/test_ednpoints.py if you face error with missing app module.)


## Tasks and Solutions:

### Task 1: Implement missing endpoint

Endpoint `GET /organisation/create/location` is missing implementation. Please implement
this endpoint for creating locations.

### Task 1 Solution:

The endpoint for location creation was successfully implemented. 
Additionally, all of endpoint paths were restructured to better align with RESTful principles.
The endpoints also follow multi-layered structure for improveed code readability.

### Task 2: Code smells

Endpoint `GET /organisation/{organisation_id}/locations` is not looking nicely.
Please fix it so that it will look more like production ready code.

### Task 2 Solution:

The endpoint was successfully refactored as a dedicated CRUD class method.
The CRUDBase class allows for full crud functionality accros all of the project models.
Additionally, the refactoring keeps the endpoint file code focused on the endpoints,
and allowed to get rid of the IDE warnings about code mismatches between output
annotations and actual CRUD function outouts.

### Task 3: Query by location

There is a new requirement that the endpoint
`GET /organisation/{organisation_id}/locations` should take an optional parameter called
`bounding_box` (tuple of 4 bounding coordinates) and should return only the locations
that are completely within the bounding box.

### Task 3 Solution:

The get_organisation_locations() endpoint was refactored according to the task,
allowing the user to input four float values which will be transformed into a bounding box.

### Task 4: Code formating

If you feel like that the code could look nicer and more readable please refactor it.

### Task 4 Solution:

The application was generally heavily restructured to better adhere to the RESTful and DRY
principles. New packages core, crud, models, and schemas allow for improved code readability
and ease of modification. The endpoints were also restructured to follow RESTful conventions,
their individual routers are now plugged in into the main parent router.
Slight changes were done to the alembic env.py to simplify Model input.

### Task 5 (Bonus): Add tests

Please add missing tests so that every endpoint is tested.

### Task 5 (Bonus) Solution:

Simple tests for the missing endpoints were added.
Use the command python tests/test_ednpoints.py from the project root directory to launch tests
if you face error with missing app module.


