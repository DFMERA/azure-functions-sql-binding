# Azure Functions SQL Binding using Python

## Introduction
This repository is a sample for Azure Functions and SQL binding extension using Python. The type of bindings in this sample are:
- **Input Binding**: takes a SQL query and a parameter to run and returns the output to the function.
- **Output Binding**: takes a list of rows and inserts them into a table (this sample was tested with an Azure SQL Database)

For more details of the different types of bindings see the [Bindings Overview](https://github.com/Azure/azure-functions-sql-extension/blob/main/docs/BindingsOverview.md).

## Prerequisites
- The [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools) version 4.x.
- Python versions that are [supported by Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages#languages-by-runtime-version). For more information, see [How to install Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- The [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for Visual Studio Code, version 1.8.3 or a later version.
- An [Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/?view=azuresql) database 

## Setup

### Install bundle
You can add the preview extension bundle by adding or replacing the following code in your host.json file:

```
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle.Preview",
    "version": "[4.*, 5.0.0)"
  }
}
```

### Update packages
Add this version of the library to your functions project with an update to the line for azure-functions== in the requirements.txt file in your Python Azure Functions project:
```
azure-functions==1.11.3b1
```

Following setting the library version, update your application settings to isolate the dependencies by adding PYTHON_ISOLATE_WORKER_DEPENDENCIES with the value 1 to your application settings. Locally, this is set in the local.settings.json file as seen below:
```
"PYTHON_ISOLATE_WORKER_DEPENDENCIES": "1"
```

### SQL connection string
Change the SQL connection string in the file local.settings.json
```
"SqlConnectionString": "Server={Azure SQL Server};Initial Catalog={Database name};Persist Security Info=False;User ID={user};Password={password};"
```

### Create table
In the database create a ToDo table:
```
CREATE TABLE dbo.ToDo (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY,
    [order] INT NULL,
    [title] NVARCHAR(200) NOT NULL,
    [url] NVARCHAR(200) NOT NULL,
    [completed] BIT NOT NULL
);
```

## Run the project

### HTTP trigger, write records to a table
The function **HttpSQLApiInsert shows a SQL output binding** in a function.json file and a Python function that adds records to a table, using data provided in an HTTP POST request as a JSON body.

The following is binding data in the function.json file:
```
...
{
    "name": "todoItems",
    "type": "sql",
    "direction": "out",
    "commandText": "dbo.ToDo",
    "connectionStringSetting": "SqlConnectionString"
}
```

Run the project and make a post request to the function HttpSqlApiInsert, you can use Postman or the test.http file in the project:
```
POST http://localhost:7071/api/HttpSqlApiInsert
content-type: application/json

[
    {
      "Id": "87de9b48-cdb5-4ca3-bf76-05c4c2a1fe92",
      "order": 1,
      "title": "Have breakfast",
      "url": "none",
      "completed": 0
    }
]
```

### HTTP trigger, get multiple rows
The function **HttpApiSelect shows a SQL input binding** in a function.json file and a Python function that reads from a query and returns the results in the HTTP response.

The following is binding data in the function.json file:
```
...
{
      "name": "todoItems",
      "type": "sql",
      "direction": "in",
      "commandText": "Select * from [dbo].[ToDo] where Id = @Id",
      "commandType": "Text",
      "parameters": "@Id={id}",
      "connectionStringSetting": "SqlConnectionString"
    }
```

Run the project and make a get request to the function HttpSqlApiSelect, you can use Postman or the test.http file in the project (remember to use the same Id you used to write the record):
```
GET http://localhost:7071/api/HttpSqlApiSelect
    ?id=87de9b48-cdb5-4ca3-bf76-05c4c2a1fe92
content-type: application/json
```
