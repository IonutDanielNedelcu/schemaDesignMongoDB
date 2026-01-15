# Sharding Tools

## Files/Directories:

	1. dump<collectionName> directories -> saved .bson versions of the initial MongoDB Atlas Database.
	2. Json<collectionName> directories -> saved .json fragmented versions of the initial MongoDB Atlas Database.
	3. _mongoDump.py -> creates a dump folder and dumps a specific collection from a specific database to a .bson file in that folder.
	4. _mongoRestore.py -> restores a specific collection from a specific database in MongoDB Atlas using a specific .bson file.
	5. _populateSharding.py -> script for uploading data to to the Docker Cluster Database.
	6. connection.py -> almost completely similar to connection.py from the 'databaseCode' folder, but instead of 'MONGO_CONNECTION_STRING' uses 'MONGO_CONNECTION_STRING_SHARDING'. Used for connecting to the Docker Cluster Database instead of the MongoDB Atlas Database.
	7. explainPipelines.json -> JSON file where all the pipelines information is dumped.
	8. explainQueries.json -> JSON file where all the query information is dumped.
	9. helpers.py -> identical copy of 'helpers.py' script from the 'queries&strategy' folder. Helper functions for query analysis.
	10. indexesDocker.py -> identical copy of 'indexes.py' script from the 'queries&strategy' folder. Why? It uses the local 'connection.py' script, which connects to the Docker Cluster instead of the Atlas Cluster.
	11. pipelinesDocker.py -> almost identical copy of 'pipelines.py' script from the 'queries&strategy' folder. Explain file path changed.
	12. runQueriesOnDocker.py -> almost identical copy of 'queries.py' script from the 'queries&strategy' folder. Explain file path changed.
	13. setupShardedCluster.py -> creates the Docker network and containers, initialises replica sets, runs mongos and registers shards.


## Usage Steps:
	1. Create the .env file and add the environment variables mentioned in Notes.
	2. Run _mongoDump for each collection from your specific database to save data (optional, but strongly recommended, to prevent data corruption)
	3. Set environment variable 'MONGO_SHARD_CONFIRM' to 'true' and open the Docker app. Run 'setupShardedCluster.py', which will create the Docker Containers we are going to use. 
	4. Run '_populateSharding.py' to populate the shards/containers created at the previous step with the data from the Json folders. (Note: instead of this, you can implement another script in the 'sharding' folder which uses the .bson files created at step 2 to populate the clusters, it's easier than this method)
	5. Run 'queriesDocker.py' to see basic queries improvement after adding strategic indexes.
	6. Run 'pipelinesDocker.py' to see aggregated pipelines improvement through successive optimisations.
    7. Analyse the explaining .json files to see detailed data about the database interogations.

### Notes:
	1. A .env file is needed, with the next environment variables:
		a. MONGO_CONNECTION_STRING -> connection string for the MongoDB Atlas Database
		b. MONGO_CONNECTION_STRING_SHARDING -> connection string to the Docker Cluster we create and are going to interogate (usually 'mongodb://localhost:27017')
		c. MONGO_SHARD_CONFIRM -> 'true'/'false', states if 'setupShardedCluster.py' should actually create the Docker Containers or just indicate commands an user would need to run