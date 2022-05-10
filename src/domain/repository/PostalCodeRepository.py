from domain.model.PostalCode import PostalCode
from abc import ABC, abstractmethod


class PostalCodeRepository(ABC):
    @abstractmethod
    def find_all_by_time_frame(self, date_from, date_to) -> [PostalCode]:
        pass

    @abstractmethod
    def find_by_did_and_time_frame(self, code: int, date_from, date_to) -> PostalCode:
        pass
