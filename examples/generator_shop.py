from typing import List

from fractal.core.event_sourcing.projectors.print_projector import PrintEventProjector
from fractal.core.process.action import Action
from fractal.core.specifications.generic.specification import Specification

from fractal_generator import generator
from fractal_generator.modeler import (
    Application,
    Command,
    Contract,
    Entity,
    Event,
    ProcessActions,
    Query,
    Repository,
    Service,
)


class GetBasketItem(ProcessActions):
    def get_process_actions(self, specification: Specification) -> List[Action]:
        from fractal.core.process.actions import FetchEntityAction

        return [
            FetchEntityAction(specification, "basket_item_repository"),
        ]


class AddBasketItem(ProcessActions):
    def get_process_actions(self) -> List[Action]:
        import uuid

        from fractal.core.process.actions import AddEntityAction

        return [
            AddEntityAction(
                id=str(uuid.uuid4()),
            ),
        ]


basket_item = Entity(
    name="BasketItem",
    fields=[
        ("id", "str"),
        ("description", "str"),
        ("quantity", "int"),
        ("unit_price_cents", "int"),
    ],
)
add_basket_item_command = Command(
    "Add",
    Event("Added"),
    Contract(
        [
            ("description", "str"),
            ("quantity", "int"),
            ("unit_price_cents", "int"),
        ]
    ),
    AddBasketItem.get_process_actions,
)
basket_item.commands.append(add_basket_item_command)
entities = [basket_item]


def generate_code():
    generator.generate(
        Application(
            name="shop",
            entities=entities,
            repositories=[
                Repository(
                    entity=entity,
                )
                for entity in entities
            ],
            internal_services=[
                Service(
                    name="Basket",
                    entity_commands=[(basket_item, add_basket_item_command)],
                    repositories=[
                        Repository(
                            entity=entity,
                        )
                        for entity in entities
                    ],
                    queries=[
                        Query(
                            name="GetBasketItem",
                            return_entity=basket_item,
                            process_actions=GetBasketItem.get_process_actions,
                        ),
                    ],
                ),
            ],
            event_projectors=[
                PrintEventProjector,
            ],
            contrib=dict(
                name="fastapi",
                # routers=["basket"],
            ),
            settings=dict(
                ALLOW_ORIGINS="",
                OPENAPI_PREFIX_PATH="",
                SENTRY_DSN="",
            ),
        )
    )


if __name__ == "__main__":
    generate_code()
