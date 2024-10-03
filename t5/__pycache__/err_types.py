# Importing the BlockErrors class from the block_errors module
from block_errors import BlockErrors  

# Define a set of error types to be handled (ZeroDivisionError and TypeError)
err_types = {ZeroDivisionError, TypeError}

# Using BlockErrors to handle specified errors
with BlockErrors(err_types):
    a = 1 / 0  # This will raise ZeroDivisionError, but it will be caught by BlockErrors
print('Completed without errors')  # This line will execute since the error is handled

# Change the error types to only handle ZeroDivisionError
err_types = {ZeroDivisionError}

# Using BlockErrors to handle specified errors
with BlockErrors(err_types):
    a = 1 / '0'  # This will raise TypeError, which is not handled by BlockErrors
print('Completed without errors')  # This line will NOT execute due to the unhandled TypeError

# Define outer error types to handle (TypeError)
outer_err_types = {TypeError}

# Using BlockErrors to handle outer error types
with BlockErrors(outer_err_types):
    inner_err_types = {ZeroDivisionError}  # Define inner error types to handle
    with BlockErrors(inner_err_types):  # Handling inner errors
        a = 1 / '0'  # This will raise TypeError, which is not handled by inner BlockErrors
    print('Indoor unit: executed without errors')  # This line will NOT execute
print('External unit: completed without errors')  # This line will execute since outer error is handled

# Define a set to handle all Exceptions
err_types = {Exception}

# Using BlockErrors to handle all types of exceptions
with BlockErrors(err_types):
    a = 1 / '0'  # This will raise TypeError, but it will be caught by BlockErrors
print('Completed without errors')  # This line will execute since the error is handled
