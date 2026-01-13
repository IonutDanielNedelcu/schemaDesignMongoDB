# Sharding tools

## Files/Directories:

	1. dump<collectionName> directories -> saved .bson versions of the initial MongoDB database (Atlas)
	2. _mongoDump.py -> creates a dump folder and dumps a specific collection from a specific database to a .bson file in that folder
	3. _mongoRestore.py -> restores a specific collection from a specific database in MongoDB Atlas using a specific .bson file
	4. connection.py -> almost completely similar to connection.py from the 'databaseCode' folder, but instead of 'MONGO_CONNECTION_STRING' uses 'MONGO_CONNECTION_STRING_SHARDING'. Used for connecting to the Docker Cluster instead of the Atlas Cluster
	5. createIndexesOnDocker.py -> identical copy of 'queriesIndexes.py' script from the 'queries&strategy' folder. Why? It uses the 'connection.py' script, which, as previously stated, connects to the Docker Cluster instead of the Atlas Cluster
	6. helpers.py -> identical copy of 'helpers.py' script from the 'queries&strategy' folder. Helper functions for query analysis
	7. runQueriesOnDocker.py -> almost identical copy of 'queries.py', the difference being at the end of the script: the output folder for 'explainQueries.json'
	8. setupShardedCluster.py -> creates the network and containers, initialises replica sets, runs mongos and registers shards
	9. explainQueries.json -> JSON file where all the query information is dumped

## Usage order:
	1. First of all, create the .env file and add the environment variables mentioned in Notes
	2. Run _mongoDump for each collection from your specific database to save data (optional, but strongly recommended, to prevent data corruption)
	3. Set environment variable 'MONGO_SHARD_CONFIRM' to 'true' and open the Docker app. Run 'setupShardedCluster.py', which will create the Docker Containers we are going to use. 
	4. Move to 'databaseCode' folder. There you will find 'Json<collectionName>' folders and '_populateSharding.py'. Running the script populates the shards/containers created at the previous step with the data from the Json folders. (Note: instead of this, you can implement another script in the 'sharding' folder which uses the .bson files created at step 2 to populate the clusters, it's easier than this method)
	5. Run 'runQueriesOnDocker.py'. This script runs the list of queries first without, and secondly with the indexes from 'createIndexesOnDocker.py', saving the data in a .json file.
	6. Be happy your code worked!!!

## Notes:
	1. a .env file is needed, containing 2 environment variables:
		a.MONGO_CONNECTION_STRING -> connection string to the initial Atlas Cluster
		b. MONGO_CONNECTION_STRING_SHARDING -> connection string to the Docker Cluster we create and are going to interogate (usually 'mongodb://localhost:27017')
		c. MONGO_SHARD_CONFIRM -> 'true'/'false', states if 'setupShardedCluster.py' should actually create the Docker Containers or just indicate commands an user would need to run