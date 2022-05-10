class PostalCode:
    def __init__(self, identity: int, code: int, geometry: str, amount: float):
        self.id: int = identity
        self.code: int = code
        self.geometry: str = geometry
        self.amount: float = amount
