# Chat With Your Data
In this stage, you will learn how to build an application that allows users to chat with their own data using Large Language Models (LLMs). The application will leverage Azure AI Foundry to create an agent that can understand user queries and provide relevant responses based on the data provided. Effectively, it is similar to stage 3, where you exposed the interface communicating to the database as a tool for LLMs.

## Setting up the Database
To get started, you need to set up a database that will store the data you want to chat with. You can use Azure SQL Database, Azure Cosmos DB, or any other database service available. As the data size is small, another option is to use SQLite database, which is a lightweight, file-based database that can be easily integrated into your application.

You will then need to ingest the data into SQLite database. You can use various methods to populate the database, such as writing scripts to insert data, using ETL tools, or getting code assistant like GitHub Copilot to help you write the data ingestion code.
Here's an example prompt you can use to get started with data ingestion using Python and SQLite:

```text
I have a CSV file containing data that I want to store in a SQLite database. Write me a sample code using Python to read the CSV file and insert the data into a SQLite database table. Create the table for me if it does not exist.
```

If you are using databases from Azure, such as Azure SQL Database or Azure Cosmos DB, you can refer to the official documentation for guidance on how to set up and populate the database:
- [Quickstart: Create an Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal)
- [Quickstart: Create an Azure PostgreSQL database](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server?tabs=portal-create-flexible%2Cportal-get-connection%2Cportal-delete-resources)
- [Quickstart: Create an Azure Cosmos DB SQL API account](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-portal)
  
Don't forget the connection string, the drivers and the authentication method needed to connect to the database from your application.

### Tools definition
Once the database is set up and populated with data, you need to define the tools that will allow the LLM to interact with the database. LLM may not understand the database, especially when the schema is not well defined. Therefore, it is important to define a data dictionary or schema that describes the structure of the database, including table names, column names, and data types. This will help the LLM to understand how to query the database effectively. This can be a standalone tool that the agent can call to get the schema information, or you can include the schema information in the system prompt when creating the agent.

Just like previous stages, you can either use Low Code or Pro Code approach to define the tools for database operations, depending on how the database is set up and your preference. If you are using Azure SQL Database or Azure Cosmos DB, you can leverage the built-in connectors in Azure Logic Apps to define the tools for database operations. If you are using SQLite database, you can use Azure AI Foundry Python SDK to create custom tools that interact with the SQLite database.