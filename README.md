# PolicyBasedAccessControl
How to Configure the project
step1 : pip install -r requirements.txt
step2 : python -m app2.seed # to get the seeded data
step3 : uvicorn app2.main:app # to run the fastapi server
step4 : visit localhost:8000/docs # to test the routes

we can check whether policies are running corretly or not by testing GET route for employees based on the data in the database
