import json
from products import get_product, Product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=data['contents'],
            cost=data['cost']
        )


def get_cart(username: str) -> list[Product]:
    """Retrieve the cart for the given username and return the product objects."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Use JSON for parsing
        except json.JSONDecodeError:
            continue  # Skip if contents are not valid JSON

        # Fetch products directly
        items.extend(get_product(product_id) for product_id in contents)

    return items


def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete the user's cart."""
    dao.delete_cart(username)
