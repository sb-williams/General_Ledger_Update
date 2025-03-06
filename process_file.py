import pandas as pd
import oracle_actions
import send_message


def process_file(src_path):

    df = pd.read_csv(src_path)

    # If the dataframe is empty or corrupt, then kill the process and send an error message.
    if df.empty:
        return False

    # delete unwanted columns
    df.drop(df.iloc[:, 0:5], inplace=True, axis=1)
    df.drop(df.iloc[:, 1:4], inplace=True, axis=1)

    # dataframe containes a few duplicates, so we need to change the names: Example; ACCOUNT.1 to ACCOUNT
    df.rename(
        columns={"DEPT.1": "DEPT", "ACCOUNT.1": "ACCOUNT", "CLASS.1": "CLASS"},
        inplace=True,
    )

    # Convert specific columns to string data types
    df["ACCOUNT"] = df["ACCOUNT"].astype(str)
    df["PROJECT"] = df["PROJECT"].astype(str)
    df["CLASS"] = df["CLASS"].astype(str)
    df["DEPT"] = df["DEPT"].astype(str)
    df["SOURCE"] = df["SOURCE"].astype(str)
    df["OU"] = df["OU"].astype(str)
    df["DOCUMENT"] = df["DOCUMENT"].astype(str)
    df["DESCRIPTION"] = df["DESCRIPTION"].astype(str)

    # PROJECT, CLASS, DEPT need to have data values changed based on a condition
    df.loc[df["PROJECT"] == "0", "PROJECT"] = "000000"
    df.loc[df["CLASS"] == "0", "CLASS"] = "0000"
    df.loc[df["DEPT"] == "0", "DEPT"] = "0000"

    # Reorder the dataframe to match the table layout in Oracle. (Mapping)
    df = df.reindex(
        [
            "CREDIT",
            "PROJECT",
            "OU",
            "DOCUMENT_DATE",
            "CLASS",
            "ACCOUNT",
            "DEBIT",
            "AMOUNT",
            "DESCRIPTION",
            "ACCOUNTINGDATE",
            "SOURCE",
            "DOCUMENT",
            "DEPT",
        ],
        axis=1,
    )

    # The ACCOUNTINGDATE and DOCUMENT_DATE fields are still a string. We need to convert it to DateTime
    # DOCUMENT_DATE
    df["DOCUMENT_DATE"] = pd.to_datetime(df["DOCUMENT_DATE"]).dt.normalize()

    # Set ACCOUNTINGDATE to the proper Datetime data type
    df["ACCOUNTINGDATE"] = pd.to_datetime(df["ACCOUNTINGDATE"]).dt.normalize()
    
    # ACCOUNTINGDATE - Grab the minimum date in the set so we can clear data from the table before appending the new data    
    # Get the minimum date from the ACCOUNTINGDATE column
    min_date_time = df["ACCOUNTINGDATE"].min()
    # We need the minimum date to be a string when we go to search for it in the table, so
    # we will first convert the min_date_time to a date object
    date_time_object = pd.to_datetime(min_date_time)
    # Convert the date objust to an standard date object without the time values
    min_date_var = date_time_object.date()
    # Take the new standard date variable to a string with the proper formatting.
    min_date = min_date_var.strftime("%d-%b-%Y")

    print(min_date)
    print(df.shape[0])
    print(df.shape[1])
    
    # The called script gets passed our min date and dataframe. It connects to Oracle, creates a 
    # backup of the table and deletes the last 6 months of data based on the min_date.
    # It will take the current dataframe values and append them to the end of file.
    run_complete = oracle_actions.backup_data(min_date, df)

    # If run_complete is successful, send message and reteurn to the main file.
    # If run is not successful, send message and generate an error.
    if run_complete == True:
        send_message.send_message(True,'FIN_GL_UPDATE Status', 'Prod & Test Tables updated successfully.')
        return True
    else:
        send_message.send_message(False,'FIN_GL_UPDATE Status', 'Prod & Test Tables update failed. Please check table and server connection.')
        return False

