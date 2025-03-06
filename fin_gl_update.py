import sys
import watchdog.events
import watchdog.observers
import time
import search_match
import process_file
import send_message

# Create a Class that will handle the event of a document being added or modified
# in the specific directory using the Watchdog library


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler. In our case it is '*.csv'
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, patterns=["*.csv"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process the new file
        # Pull the date from the file name and validate that it is the correct Month and Year. Store the return value to search_complete
        time.sleep(20)
        search_complete = search_match.pull_date(event.src_path)
        try:
            search_complete == True
        except Exception:
            send_message(
                False, "Date Mismatch", "Extract file is older than the current date."
            )
            observer.stop()
            sys.exit(0)

        if search_complete == True:
            complete_process = process_file.process_file(event.src_path)
            #If everything works, then kill watchdog process and end script cleanly
            if complete_process == True:
                observer.stop()
                sys.exit(0)
            else:
                try:
                    complete_process == False
                except Exception:
                    observer.stop()
                    sys.exit(0)


# Turn the Watchdog on. Create an instanace of the Handler class once the script is launched.
# The processing of the CSV and tables will also be handled from within the class instance.

if __name__ == "__main__":
    src_path = r"C:\inbound"
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)

    observer.start()
    print("Watchdog running")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
