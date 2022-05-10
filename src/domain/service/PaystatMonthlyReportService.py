from datetime import datetime

from domain.repository.PaystatMonthlyReportRepository import PaystatMonthlyReportRepository


class PaystatMonthlyReportService:
    def __init__(self, repository: PaystatMonthlyReportRepository):
        self.repository = repository

    def get_by_time_frame(self, date_from, date_to):
        return self.repository.find_by_time_frame(date_from, date_to)

    def get_aggregated_by_time_frame_and_postal_code(self,date_from: datetime, date_to: datetime, postal_code: int):
        return self.repository.get_aggregated_by_time_frame_and_postal_code(date_from, date_to, postal_code)

