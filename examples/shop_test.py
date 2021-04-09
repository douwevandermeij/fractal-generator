from fractal.core.specifications.generic.operators import EqualsSpecification

from shop.domain.contracts import AddBasketItemContract
from shop.main import ShopFractal


if __name__ == '__main__':
    a = ShopFractal.context.basket_service.add_basket_item(
        AddBasketItemContract(
            description="a",
            quantity=1,
            unit_price_cents=95,
        )
    )
    b = ShopFractal.context.basket_service.add_basket_item(
        AddBasketItemContract(
            description="b",
            quantity=1,
            unit_price_cents=95,
        )
    )
    aa = ShopFractal.context.basket_service.get_basket_item(EqualsSpecification("id", a.id))
    print(aa)
