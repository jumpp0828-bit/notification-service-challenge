import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable

from app.services.util import generate_unique_id


class NotificationError(Exception):
    pass
class ChannelUnavailableError(NotificationError):
    pass
class DeliveryError(NotificationError):
    pass


class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class ConsoleChannel(NotificationChannel):

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError("Console channel not available")

        try:
            print(message)
        except Exception as e:
            raise DeliveryError(f"Error printing message: {e}")

    def get_channel_name(self) -> str:
        return "console"

    def is_available(self) -> bool:
        return True

class FileChannel(NotificationChannel):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def is_available(self) -> bool:
        directory = os.path.dirname(self.file_path) or "."

        if os.path.isdir(directory) and os.access(directory, os.W_OK):
            return True


        if os.path.isfile(self.file_path) and os.access(self.file_path, os.W_OK):
            return True

        return False