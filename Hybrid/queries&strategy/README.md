# Querying & Optimization Strategies

## Files/Directories:
    1. connection.py -> connection.py -> MongoDB connection helper used by the scripts.
    9. explainPipelines.json -> JSON file where all the pipelines information is dumped
    9. explainQueries.json -> JSON file where all the query information is dumped
    4. helpers.py -> helper functions for query/pipeline analysis
    5. indexes.py -> helper script for creating indexes on database collections
    6. pipelines.py -> runs pipelines with different configurations/optimisations and saves the results in 'explainPipelines.json'
    7. queries.py -> runs queries with&without indexes and saves the results in 'explainQueries.json'


## Usage Steps:
    1. Create the .env file and add the environment variables mentioned in Notes.
    2. Run 'queries.py' to see basic queries improvement after adding strategic indexes.
    3. Run 'pipelines.py' to see aggregated pipelines improvement through successive optimisations.
    4. Analyse the explaining .json files to see detailed data about the database interogations.


### Notes:
    1. A .env file is needed, with the next environment variables:
        a. MONGO_CONNECTION_STRING -> connection string for the MongoDB Atlas Database.