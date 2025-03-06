# General_Ledger_Update

This Python project was created to take data from a CSV file, clean it, transform the data, and update a master Oracle table.

This master oracle table is used with several Tableau Dashboards.

The project uses a Watchdog library to look for the creation of the csv file. Once that action occurs, it takes the file and imports into a Pandas dataframe for ETL processing, loads the data, and then
sends an email to the Analytics team.
