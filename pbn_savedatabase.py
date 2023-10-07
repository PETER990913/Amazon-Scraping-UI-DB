import datetime

# Get the current date and time
now = datetime.datetime.now()

time = now.strftime("%Y-%m-%d %H:%M:%S")

# Print the current date and time in a specific format
print("Current Date and Time:", time)