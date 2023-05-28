# Decision Optimization in the Entertainment Industry: Data Analytics and Process Modeling at Netflix.

## Introduction

In this project, I have deepened in the theoretical concepts related to data analysis and decision making. Throughout this process, I have applied my knowledge to design and build an information system to make informed decisions.

First, I focused on modeling the business process for deciding whether to produce a series, movie or not. I used UML and BPMN activity diagrams to visually represent this process and make it easier to understand. This model is not the one that would finally be applied but it shows what would be the process of selecting a film or series.

As a next step, I performed analysis of the raw data from the Netflix platform. I analyzed the consumption data of some users and created bar charts to present the information visually and facilitate decision making by executives.

In summary, throughout this personal project I have created an information system that integrates data analysis and decision making. I have applied the theoretical knowledge acquired to:

- Design and build a data warehouse.
- Manipulate data and perform analytical operations.
- Develop a Balanced Scorecard (BSC) to support business decision making.

This project has been an opportunity to autonomously apply the theoretical concepts learned and get a more practical view of their application in a business context.

## Process modeling

So far, I have started by modeling the business process I have been tasked with on this project. The business process focuses on the decision to produce a series or movie when a scriptwriter submits a proposal. To visualize and represent this process, I created a UML diagram that shows all the stages and the interactions between the different actors involved.

Here is the resulting UML diagram:

![UML](images/UML.png) 

On the other hand, the resulting BPMN diagram is:

![BPMN](images/BPMN.png) 

Both diagrams accurately captures the workflow and key activities necessary to evaluate the writer's proposal and make an informed decision. It provides a clear and concise view of the steps involved, from script review to financial evaluation and final decision making.

## MIS (Management Information System)

FILE: [TransactionalProcess](https://github.com/pizarroiker/SI-P1/blob/master/Transaccional/TransactionalProcess.py)

During this stage of the project, a first version of a management information system was developed. To achieve this, I obtained a .csv file provided by Kaggle containing data from different Netflix movies and series, which I had to transform to a format suitable for further processing using a high-level programming language.

In my case, I decided to work with Python using the pandas library, widely recognized and currently used for data analysis. To store the information efficiently, I chose to use SQLite3 as a database, since it offers all the necessary features to meet the requirements of the project, in addition to presenting ease of use and integration, as it is an embedded database. Finally, to create the graphics, I selected the matplotlib library.

### Creation of the Database

In the first phase, I focused on reading the data from the .csv files and storing them in the database. In the first phase, I focused on reading the data from the .csv files, and then storing it in the database. I had to take into account that some rows of the .csv file contained empty fields, so I had to indicate to the conversion function that, in these cases, the data would be stored in the database with the value NULL. To store this data, I created a table called "show" in the relational database. To read the data, I used the pandas read_csv function, which returned a pandas DataFrame that we later converted into a SQLite3 table using to_sql. In this way, we obtained our "show" table with all the data of the series and movies, located in the [TransactionalDatabase.db](https://github.com/pizarroiker/SI-P1/blob/master/DDBB/TransactionalDatabase.db)

In the context of this project, the most relevant data for a streaming platform like Netflix are those related to the viewing of the different contents. Since we did not have access to that real information, I had to simulate the viewing of several users in relation to the available content. This allowed me to perform a data analysis in the next step and test it with fictitious data before applying it to real user data.

To carry out this simulation, first, it was necessary to generate users using the [generateCsvUsers.py](https://github.com/pizarroiker/SI-P1/blob/master/Transaccional/CSV/generateCsvUsers.py) file and create a table in the database to store them, following the same process used for the Netflix CSV file. In this table, we store the user's ID, name, last login date and country. 

Once all the users were generated, I proceeded to randomly generate the users viewing data for the different contents. To accomplish this, I generate a csv with randomly generated data and manipulate some entries to try to simulate real data in the later phases( using [generateCsvViews.py](https://github.com/pizarroiker/SI-P1/blob/master/Transaccional/CSV/generateCsvViews.py)). Later I created the table in the database, this one includes the following fields: id (to identify the viewing), id_show (to identify the content viewed), id_user (to identify the user who viewed it), date (to identify when the view took place) and score (representing the rating given by the user to the content).

### Database queries and statistics

FILE: [Report](https://github.com/pizarroiker/SI-P1/blob/master/Transaccional/report.html)

The first thing I did was to divide the shows table into a series of dataframes. The importance of this work lies in the organization's need to analyze and make decisions based on relevant and segmented information. For this, I classified the data into movies and series. Then, I grouped series by number of seasons and movies by length. This has made a certain section of the report much easier to perform. After doing this, the program will create an html report where we will show statistics of the show table and the dataframes mentioned above.

I performed several calculations to obtain relevant information about the data. First, I calculated the number of available samples, considering those entries that had no empty fields. In addition, I determined the maximum and minimum value of the launch year. I used the launch date as a reference and filtered out those empty fields to avoid problems with null values. This gave us a clear idea about the temporal distribution of the analyzed data. Continuing with the analysis, I focused on the duration values. For both movies and series, we performed specific calculations. I filtered out the null duration values as I considered that these values were not relevant and could affect the final results.

These calculations were implemented using SQL queries and we used functions from the pandas library to manipulate and process the data efficiently. These are the results reflected in the report:


| Query                     | Result                           | 
| ------------------------- | --------------------------------- | 
| Number of complete samples (without missing values)   | 5747   | 
| Average duration (Movies)      | 100 minutes       |
| Average duration (TV Shows) | 2 seasons  | 
| Standard deviation of duration (Movies) | 28.29   | 
| Standard deviation of duration (TV Shows) | 1.58   | 
| Maximum Movie duration | 312 minutes  | 
| Maximum TV show duration | 17 seasons   | 
| Minimum Movie duration | 3 minutes |
| Minimum TV show duration | 1 seasons  | 
| Most recent year of publication | 2021   | 
| Oldest year of publication | 1925 |

Returning to the previous dataframes, we have performed on each one a series of operations to obtain statistical data for each one. As before, all these data have been compiled in the report. Tables with the results obtained are shown below.


#### Type of Content


| | Movies |              
| ------- | -------- |
| Length | 6131   |      
| Null Values | 3      |     
| Median | 98.0  |     
| Mean | 99.58   |   
| Var | 800.36  |  
| Maximum | 312.0 |   
| Minimum | 3.0   |   


| | TV Shows |
| ------- | ------- | 
| Length | 2676   | 
| Null Values | 0   |
| Median | 1.0  |
| Mean | 1.76   |
| Var | 2.51  |
| Maximum | 17 |
| Minimum | 1   | 


#### Type of Movie


| | Movies that are longer than 90 minutes or 90 minutes long |              
| ------- | -------- |
| Length | 4290   |          
| Median | 107.0  |     
| Mean | 112.45   |   
| Var | 434.69  |  
| Maximum | 312 |   
| Minimum | 90   |   


| | Movies that last less than 90 minutes |
| ------- | ------- | 
| Length | 1838   | 
| Median | 76.0  |
| Mean | 69.53   |
| Var | 364.24  |
| Maximum | 89 |
| Minimum | 3   | 


#### Type of TV Show


| | TV Shows that last more than 2 seasons |              
| ------- | -------- |
| Length | 458   |        
| Median | 4.0  |     
| Mean | 4.54   |   
| Var | 4.59 |  
| Maximum | 17 |   
| Minimum | 3 |   


| | TV Shows that last 2 seasons or less |
| ------- | ------- | 
| Length | 2218   | 
| Median | 1.0  |
| Mean | 1.19   |
| Var | 0.15  |
| Maximum | 2 |
| Minimum | 1   | 

These results could provide the organization important information about the distribution and temporal range of the analyzed data, which allows us to move forward in the project with a better understanding of the situation.


### Plots

At this stage of the project, I have recognized the importance of presenting the information in a visual and easily understandable way. To achieve this, I have chosen to use bar charts, which allow a clear and concise visualization of the data.

By using bar charts, we are prioritizing clarity and ease of understanding the data. This allows us to effectively communicate the results of the analysis and provide an overview of the most popular movies in terms of views.

One of the first graphs created is the top 10 most viewed movies. This bar chart shows in an orderly and hierarchical way the movies that have been most viewed, allowing us to quickly identify which are the most popular. This visual approach facilitates the interpretation of the information and helps most people to understand it in a simple way.

![Movies Most Views](images/GraficoMoviesMostViews.png)

In line with our visual and comprehensible approach, we have extended the use of bar charts to represent the top 10 most viewed series. This new chart allows us to clearly and concisely visualize the most popular series in terms of number of views.

![TV Shows Most Views](images/GraficoTVShowsMostViews.png)

In the final stage of this analysis, I compared content by duration, focusing on movies. To do so, I calculated the average number of views for movies with a duration of more than 90 minutes and the average number of views for movies with a duration of less than 90 minutes.

![Average Type of Movies](images/AverageMovies.png)

I have done the same for TV Shows, comparing the average viewings of those with 2 or less seasons with those with more than 2 seasons.

![Average Type of TV Shows](images/AverageShows.png)


## Data Warehouse

### Data warehouse Design

In this phase, I have explored the theoretical concepts related to the design of a data warehouse. I have followed a series of steps to establish the basis of my design:

First, I have selected the central fact for my data warehouse, which is "Visualizations". Later, I will define the measures associated with this fact.

Next, I have identified the dimensions needed to address the issues raised. I have found the following relevant dimensions: a temporal dimension (mandatory) that will provide information about when the visualizations were performed, a "Show" dimension that will provide details about the movies or series visualized, and a "User" dimension that will indicate who performed the visualizations. 

Then, I decided on the granularity for each of the dimensions. I have chosen to follow the atomic granularity in the "Show" dimension, as this will allow me to get all the information from the shows and present it in various forms. As for the "Time" dimension, I have decided to drill down only to months, considering that this information is sufficient for the tasks to be performed. Finally, in the "User" dimension, as in the "Item" dimension, I have opted for atomic granularity, including all user attributes.

To complete the design of my data warehouse, I must select the measures and attributes related to the core fact and dimensions. The core measures for the fact "Visualizations" will be the total number of visualizations performed and the average ratings of these. As for the attributes, in the dimension "Time" I have decided to include the attributes of year and month. On the other hand, the "Item" dimension will contain all the fields of the "shows" table of my transactional database, and the "User" dimension will contain all the fields of the "users" table.

Regarding the tables, I have considered the following:

First, the "Time" table can be created and filled in directly, since we know in advance its structure and the information it will contain. In this case, I have decided to count the visualizations made from the beginning of January 2018 to April 2023, covering a period of approximately 5 years.

On the other hand, the "Show" table will be identical to the "Shows" table in our transactional database, as it contains the relevant details of the movies or series viewed. Likewise, the "User" dimension will match the users table in our transactional database, as it provides information on who performed the views.

In addition, I have reflected on the need for external information for the development of our data warehouse. I came to the conclusion that, although it is advisable to use internal and external sources, in this case I do not require additional information beyond what I already have in our transactional database to address the questions posed.

As for the choice of approach, I have chosen to use ROLAP and have designed our data warehouse following a star model. Below, I present the warehouse design, where the text fields are represented as VARCHAR2, as that was the option selected for "String" in the modeling tool used. The rows marked with "P" indicate the primary keys, while those marked with "F" represent the foreign keys. The arrows used simply indicate association by foreign keys, without regard to cardinality or other specifics. It is important to note that this design is a preliminary representation of the warehouse in SQL format and may undergo modifications during the implementation process.

![Star Model](images/model.png)

### Warehouse construction and ETLs

FILE: [Data Warehouse Construction and loading](https://github.com/pizarroiker/SI-P1/blob/master/Datawarehouse/CreateDW.py)
