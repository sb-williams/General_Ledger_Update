import re
from datetime import datetime
from dateutil import parser

def pull_date(src_path):

    # Search for the date in the file name, clean and format it.
    date_in_file = re.search(r'\d{2}_\d{2}_\d{4}', src_path).group(0)
    clean_file_date = re.sub('_', '-', date_in_file)
    file_date = parser.parse(clean_file_date, dayfirst=True)

    # if the month and date found in the file match the current month and year, we can move forward with processing
    if file_date.month == datetime.now().month and file_date.year == datetime.now().year:
        # Process the file
        return True
    else:
        # Don't process the file
        return False

