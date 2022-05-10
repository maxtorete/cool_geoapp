from datetime import datetime

from domain.model.PaystatMonthlyReport import PaystatMonthlyReport
from abc import ABC, abstractmethod


class PaystatMonthlyReportRepository(ABC):
    @abstractmethod
    def find_by_time_frame(self, date_from, date_to) -> [PaystatMonthlyReport]:
        pass

    @abstractmethod
    def get_aggregated_by_time_frame_and_postal_code(self, date_from: datetime, date_to: datetime,
                                                     postal_code: int) -> [PaystatMonthlyReport]:
        pass
