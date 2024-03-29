# Database Schema
The model management service stores all data in a PostgreSQL database.  The schema consists of four tables, corresponding to the four types of resources (projects, parameter sets, trained models, and model tests).

![Database Schema](database_schema.png)

## Projects
All parameter sets, models, and test results are organized by project.  The Projects table stores an integer identifier (primary key) and name.

## Parameter Sets
Parameter sets are the configuration information needed to train a model on raw input data.

For example, in Scikit-Learn parlance, the parameter set would define any transformers (e.g., text vectorizers and scalers), the model class, and any parameters needed for instantiation.  It is assumed that a batch training job would pull all active parameter sets, train models for each, and upload those models through the service.

## Trained Models
Trained models are the serialized transformer and model parameters from training.

Through the `training_data_from` and `training_data_until` properties, the table records the date range of the data used in training.  It is assumed that a production system will train a model on data from some immediately previous time frame such as the previous 30 days.  This might be shifted (e.g., data from -30 to -2 days).

Similarly, it is assumed that models will be retrained on a regular basis (e.g., every day).  To effectively "version" the models, the table supports a training date/time.

Like the parameter sets, the trained models have a concept of a deployment stage.  Valid values include `testing`, `production`, and `retired`.

## Model Tests
It is assumed that most production systems will run sanity checks on trained models before deploying them to production.  For example, data for a subset of users might be excluded from training.  The model might then be tested on data for those excluded users.  Deployment of the model would be gated on passing the sanity checks.

The table stores the date/time of the test, the test results, and a flag indicating whether the evaluations met the user-defined criteria.

## Note on Object Serialization
JSON is used by the REST API to exchange data.  JSON does not support a binary or bytes type, so strings are used to store the serialized objects.  These values are stored directly in the database as text.  It might be better to store the serialized objects as binary strings in the database (e.g., using the bytea type).

## Metadata
Every object also supports using JSON metadata, which can be passed in as an empty dictionary if it is unused. Otherwise, it can be used to store any additional information needed.

