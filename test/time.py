from datetime import datetime, timedelta

def check_time_condition():
  # Get the current time
  current_time = datetime.now().time()

  # Set the desired time (07:30:00)
  desired_time = datetime.strptime('07:30:00', '%H:%M:%S')

  # Add a time delta of 30 minutes to the desired time
  desired_time_with_delta = (datetime.combine(datetime.today(), desired_time) + timedelta(minutes=30)).time()

  print("Current time: " + str(current_time))
  print("Desired time: " + str(desired_time))
  print("Desired time with delta: " + str(desired_time_with_delta))

  # Check if the current time is greater than the calculated desired time with delta
  if current_time > desired_time_with_delta:
    print("Current time is greater than 07:30:00 + 00:30:00.")
  else:
    print("Current time is not greater than 07:30:00 + 00:30:00.")

# Call the function
check_time_condition()
