from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable, Type, Dict

from dill.source import getsource

from fractal.core.event_sourcing.event_projector import EventProjector
from fractal.core.process.action import Action
from fractal.core.utils.string import camel_to_snake


@dataclass
class MetaMetaModel:
    pass


@dataclass
class Application(MetaMetaModel):
    name: str
    entities: List['Entity'] = field(default_factory=list)
    repositories: List['Repository'] = field(default_factory=list)
    internal_services: List['Service'] = field(default_factory=list)
    ingress_services: List['Service'] = field(default_factory=list)
    egress_services: List['Service'] = field(default_factory=list)
    event_projectors: List[Type[EventProjector]] = field(default_factory=list)
    contrib: Dict = field(default_factory=dict)
    settings: Dict = field(default_factory=dict)


@dataclass
class Service(MetaMetaModel):
    name: str
    entity_commands: List[Tuple['Entity', 'Command']] = field(default_factory=list)
    repositories: List['Repository'] = field(default_factory=list)
    queries: List['Query'] = field(default_factory=list)


@dataclass
class Repository(MetaMetaModel):
    entity: 'Entity'


@dataclass
class Entity(MetaMetaModel):
    name: str
    fields: List[Tuple[str, str]]
    commands: List['Command'] = field(default_factory=list)


@dataclass
class Aggregate(MetaMetaModel):
    name: str


@dataclass
class Contract(MetaMetaModel):
    fields: List[Tuple[str, str]]


@dataclass
class Command(MetaMetaModel):
    name: str
    event: 'Event'
    contract: Contract
    process_actions: Optional[Callable] = None


@dataclass
class Query(MetaMetaModel):
    name: str
    return_entity: Entity
    process_actions: Optional[Callable] = None

    @property
    def process_actions_source(self):
        if not self.process_actions:
            return None
        return getsource(self.process_actions).replace(
            "def get_process_actions(self",
            f"def __get_process_actions_{camel_to_snake(self.name)}(self",
        )


@dataclass
class Event(MetaMetaModel):
    name: str


@dataclass
class Actor(MetaMetaModel):
    name: str


class ProcessActions(ABC):
    @abstractmethod
    def get_process_actions(self, *args, **kwargs) -> List[Action]:
        raise NotImplementedError
