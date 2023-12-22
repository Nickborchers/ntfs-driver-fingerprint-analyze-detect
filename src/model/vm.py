from abc import ABC, abstractmethod
import subprocess
import time
import logging
from command import run
from model.os import OS

WAIT_SECONDS = 5

class VM(ABC):
    """Abstract base class that represents a VirtualBox VM."""
    def __init__(self, type: OS, name: str, username: str, password: str):
        self.type = type
        self.name = name
        self.username = username
        self.password = password

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def execute_command(self, command: str) -> None:
        pass

    def __repr__(self) -> str:
        return str(self.__dict)
