import os
import oracledb
from dotenv import load_dotenv


def backup_data(min_date, df):

    load_dotenv()
    # Connect to a database using the env variable
    conn_test = oracledb.connect(
        user=os.environ.get("DATA_KEY"),
        password=os.environ.get("DATA_SECRET"),
        host=os.environ.get("DATA_HOST"),
        port=os.environ.get("DATA_PORT"),
        service_name=os.environ.get("SERVICE_NAME"),
    )

    conn_prod = oracledb.connect(
        user=os.environ.get("DATA_KEY"),
        password=os.environ.get("DATA_SECRET"),
        host=os.environ.get("DATA_HOST2"),
        port=os.environ.get("DATA_PORT2"),
        service_name=os.environ.get("SERVICE_NAME"),
    )

    # If the connection fails, cancel the update and send a failure message.
    if not conn_test or not conn_prod:
        return False
    else:

        # A cursor is used to send SQL actions to the table
        cursor_test = conn_test.cursor()
        cursor_prod = conn_prod.cursor()

        # Create backup of table with today's date
        # Test
        cursor_test.execute(
            """BEGIN EXECUTE IMMEDIATE 'create table FIN_GL_ACTUALS_'||to_char(sysdate, 'DD_MON_YYYY')||' as SELECT * FROM FIN_GL_ACTUALS'; END;"""
        )
        # Prod
        cursor_prod.execute(
            """BEGIN EXECUTE IMMEDIATE 'create table FIN_GL_ACTUALS_'||to_char(sysdate, 'DD_MON_YYYY')||' as SELECT * FROM FIN_GL_ACTUALS'; END;"""
        )

        print("backups created")

        # Delete the data based on the min_date.
        # Test
        cursor_test.execute(
            "DELETE FROM FIN_GL_ACTUALS WHERE TRUNC(ACCOUNTINGDATE) >= :mybv",
            mybv=min_date,
        )
        # Prod
        cursor_prod.execute(
            "DELETE FROM FIN_GL_ACTUALS WHERE TRUNC(ACCOUNTINGDATE) >= :mybv",
            mybv=min_date,
        )

        # Save the changes to the table after deleting
        conn_test.commit()
        conn_prod.commit()

        # Append the data from the dataframe to the table
        rows = [tuple(x) for x in df.values]
        cursor_test.executemany(
            "INSERT INTO FIN_GL_ACTUALS VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)",
            rows,
        )
        cursor_prod.executemany(
            "INSERT INTO FIN_GL_ACTUALS VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)",
            rows,
        )

        # Save the appended records to the table.
        conn_test.commit()
        conn_prod.commit()

        print("tables updated")

        # Close the connection and cursor to the table and database for security reasons.
        cursor_test.close()
        cursor_prod.close()
        conn_test.close()
        conn_prod.close()

        return True
