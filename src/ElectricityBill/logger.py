# import logging
# import os
# import sys
# from datetime import datetime

# # Define the logfile name using the current date and time
# log_file_name = f"{datetime.now().strftime('%m_%d_%H_%M_%S')}.log"

# # Create the path to the log file inside the log directory
# log_file_path = os.path.join(os.getcwd(), "logs", log_file_name)

# # Create the log directory if it does not exist
# os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# # Configure basic logging settings
# logging.basicConfig(
#     #filename=log_file_path,  # Set the filename for logging
#     format="[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Define log format
#     level=logging.INFO,  # Set logging level to DEBUG
#     handlers=[
#         logging.FileHandler(log_file_path),  # Output logs to file
#         logging.StreamHandler(sys.stdout)  # Output logs to console
#     ]
# )

# logger = logging.getLogger("ElectricityBill")