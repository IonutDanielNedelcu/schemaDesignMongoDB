# Schema Design Strategies and Scaling Solutions in MongoDB in E-Commerce

## Data Modeling & Collection Organization
&nbsp;&nbsp;&nbsp;&nbsp;This section outlines the main schema-design approaches for e-commerce data in MongoDB and explains how to choose between embedding, referencing, or a hybrid model based on access patterns, update frequency, and document size.

- #### MongoDB versus SQL Approaches

&nbsp;&nbsp;&nbsp;&nbsp;Mongo

&nbsp;

### 1. Modeling Strategies


- ##### Embedding Strategy

![Embedding model diagram](_materials/embeddingDiagram.png)

&nbsp;&nbsp;&nbsp;&nbsp;Schema choice - am vrut sa construim o baza de date cat mai departata conceptual de SQL databases


- ##### Referencing Strategy

![Referencing model diagram](_materials/referencingDiagram.png)

&nbsp;&nbsp;&nbsp;&nbsp;Schema choice - am vrut sa vedem si o varianta cat se poate de apropiata de SQL


- ##### Hybrid Strategy

![Hybrid model diagram](_materials/hybridDiagram.png)

&nbsp;&nbsp;&nbsp;&nbsp;Schema choice - imbinarea dintre cele 2 - uneori util embedding, alteori referencing, alteori amandoua


### 2. Comparative Analysis

| Aspect | Embedding | Referencing | Hybrid |
|---|---|---|---|
| Data Consistency | | | |
| Data Redundancy | | | |
| Performance | | | |
| Flexibility | | | |

&nbsp;

## CRUD Operations

&nbsp;&nbsp;&nbsp;&nbsp;Due the project focus, only the base-level CRUD operations were implemented for each collection (create, find-one, find-all, update-one, delete-one). Users can use the "input" and "jsonCollectionStructure" files as input guides for CRUD operations.

&nbsp;

## Optimization Strategies

### 1. Queries

&nbsp;&nbsp;&nbsp;&nbsp;First we ran queries without indexes. 10 of them
> Queries List:
> Q1: 
> Q2: 
> Q3: 
> Q4: 
> Q5: 
> Q6: 
> Q7: 
> Q8: 
> Q9: 
> Q10: 


&nbsp;

### 2. Pipelines

&nbsp;&nbsp;&nbsp;&nbsp;First we ran pipelines without indexes. 3 of them
> Pipelines List:
> P1: 
> P2: 
> P3: 

&nbsp;

### 3. Indexes

&nbsp;&nbsp;&nbsp;&nbsp;Added 10 strategic indexes. Queries & Pipelines performance after adding indexes
> Common Indexes List:
> I1: 
> I2: 
> I3: 
> I4: 

Note: even though common indexes have different database implementations (i.e collection/field/structural differences due to database structure differences), they have and serve the same database logic.


&nbsp;
- ##### Embedding Database
> Database-Level Indexes List:
> I1: 
> I2: 
> I3: 
> I4: 

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

&nbsp;

- ##### Referencing Database
> Database-Level Indexes List:
> I1: 
> I2: 
> I3: 
> I4: 

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

&nbsp;

- ##### Hybrid Database
> Database-Level Indexes List:
> I1: 
> I2: 
> I3: 
> I4: 

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

&nbsp;

## Scaling Strategies

### 1. Vertical Scaling (Scale Up)

&nbsp;&nbsp;&nbsp;&nbsp;Vertical scaling (scale up) means

### 2. Horizontal Scaling (Sharding)

&nbsp;&nbsp;&nbsp;&nbsp;Horizontal scaling (sharding) refers to

&nbsp;&nbsp;&nbsp;&nbsp;For our databases, we decided to split the databases in 3 shards each.


- ##### Embedding Database Sharding

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

&nbsp;

- ##### Referencing Database Sharding

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

&nbsp;

- ##### Hybrid Database Sharding

| Querying | Without Indexes | With Indexes |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |
| Q5 | | |
| Q6 | | |
| Q7 | | |
| Q8 | | |
| Q9 | | |
| Q10 | | |

| Querying | Inefficient Without Indexes | Inefficient With Indexes | Efficient With Indexes|
|---|---|---|---|
| P1 | | | |
| P2 | | | |
| P3 | | | |

