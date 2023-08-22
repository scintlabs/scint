from util.logging import logger


class Observer:
    """Observer class."""

    def __init__(self) -> None:
        logger.info(f"Initializing observer.")
        self.site_data = ["Upwork", "Twitter", "LinkedIn"]
        self.email_observer()
        self.messaging_observer()
        self.site_observer(self.site_data)

    def email_observer(self):
        logger.info(f"Email observer active.")

    def messaging_observer(self):
        logger.info(f"Messaging observer active.")

    def site_observer(self, data):
        logger.info(f"Site observer active, monitoring: {str(self.site_data)}.")
