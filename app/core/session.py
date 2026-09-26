class SessionManager:
    """
    Manage user session data for the application.
    """

    def __init__(self):
        """
        Initialize an empty session storage.

        Returns:
            None
        """
        self.sessionData = {}

    def set(self, key, value):
        """
        Store a value in the session.

        Args:
            key (str): Session key.
            value: Value to store.

        Returns:
            None
        """
        self.sessionData[key] = value

    def get(self, key, default=None):
        """
        Retrieve a value from the session.

        Args:
            key (str): Session key.
            default: Value returned if key does not exist.

        Returns:
            Any: Stored session value or default value.
        """
        return self.sessionData.get(key, default)

    def remove(self, key):
        """
        Remove a value from the session.

        Args:
            key (str): Session key to remove.

        Returns:
            None
        """
        self.sessionData.pop(key, None)

    def clear(self):
        """
        Clear all session data.

        Returns:
            None
        """
        self.sessionData.clear()