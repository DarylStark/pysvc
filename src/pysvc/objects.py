"""Module that contains all possible objects."""
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union


@dataclass
class SVCObject(ABC):
    """Base class for all objects."""

    @abstractmethod
    def get_object_hash(self) -> str:
        """Calculate the hash of the object."""

    @abstractmethod
    def get_object_contents(self) -> str:
        """Get the contents of the object."""


@dataclass
class File(SVCObject):
    """A file on the disk."""

    contents: str

    def get_object_hash(self) -> str:
        """Calculate the hash of the file."""
        sha1_hash = hashlib.sha1(self.contents.encode()).hexdigest()
        return sha1_hash[2:]

    def get_object_contents(self) -> str:
        """Get the contents of the file."""
        return self.contents


@dataclass
class Tree(SVCObject):
    """A directory on the disk.

    Contains leave objects or other trees.
    """

    objects: dict[str, Union[File, 'Tree']] = field(default_factory=dict)

    def get_object_hash(self) -> str:
        """Calculate the hash of the file."""
        contents_to_hash = ''.join(
            [
                f'{filename}{obj.get_object_hash()}'
                for filename, obj in sorted(self.objects.items())
            ]
        )
        sha1_hash = hashlib.sha1(contents_to_hash.encode()).hexdigest()
        return sha1_hash[2:]

    def _get_object_type(self, obj: SVCObject) -> str:
        """Return the object type for a given object."""
        object_types: dict[object, str] = {File: 'blob', Tree: 'tree'}
        if object_types.get(type(obj)) is None:
            raise ValueError(f'Unknown object type: {type(obj)}')
        else:
            return object_types[type(obj)]

    def get_object_contents(self) -> str:
        """Get the contents of the file."""
        return '\n'.join(
            [
                f'{filename}\t{self._get_object_type(obj)}\t{obj.get_object_hash()}'
                for filename, obj in sorted(self.objects.items())
            ]
        )


@dataclass
class Commit(SVCObject):
    """A commit object."""

    tree_hash: str
    message: str
    parents: list['Commit'] | None = None

    def get_object_hash(self) -> str:
        """Calculate the hash of the file."""
        contents_to_hash = f'{self.tree_hash}_{self.message}'
        sha1_hash = hashlib.sha1(contents_to_hash.encode()).hexdigest()
        return sha1_hash[2:]

    def get_object_contents(self) -> str:
        """Get the contents of the file."""
        return (
            f'Commit {self.get_object_hash()}\n'
            + f'Parent commit: {self.parents}\n'
            + f'Tree: {self.tree_hash}\n\n'
            + f'Message: {self.message}'
        )
