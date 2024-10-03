class BlockErrors:
    """A context manager to selectively suppress specified exception types."""

    def __init__(self, err_types) -> None:
        """
        Initializes the BlockErrors context manager.

        Parameters:
        err_types (tuple): A tuple of exception types to be suppressed.
        """
        self.err_types = err_types
    
    def __enter__(self):
        """Enters the runtime context and returns None."""
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context, handling exceptions based on their types.

        Parameters:
        exc_type (type): The type of the exception raised.
        exc_val (Exception): The exception instance.
        exc_tb (traceback): The traceback object.

        Returns:
        bool: True if the exception is to be suppressed; False otherwise.
        """
        # Check if the exception type is in the specified error types
        if exc_type not in self.err_types and not any(issubclass(exc_type, i) for i in self.err_types):
            # If not, propagate the exception
            return False
        else:
            # Suppress the exception
            return True
