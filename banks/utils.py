from typing import Optional



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Address:
    def __init__(self, street: Optional[str] = None, city: Optional[str] = None, region: Optional[str] = None,
                 postal_code: Optional[int] = None, country: Optional[str] = None):
        self.street = street
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country = country

    def validate(self) -> bool:
        if self.street is not None and self.city is not None and self.region is not None and \
                self.postal_code is not None and self.country is not None:
            return True
        else:
            return False


class UniqueIdGeneratorSingleton(metaclass=Singleton):
    def __init__(self):
        self.curr_id = 0

    def generate_new_unique_id(self) -> int:
        self.curr_id += 1
        return self.curr_id


def get_unique_id() -> int:
    return UniqueIdGeneratorSingleton().generate_new_unique_id()
