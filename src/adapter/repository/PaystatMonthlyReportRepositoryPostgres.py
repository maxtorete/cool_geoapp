from datetime import datetime

from domain.model.PaystatMonthlyReport import PaystatMonthlyReport
from domain.repository.PaystatMonthlyReportRepository import PaystatMonthlyReportRepository
from adapter.database.postgres import pg_connection


class PaystatMonthlyReportRepositoryPostgres(PaystatMonthlyReportRepository):
    def find_by_time_frame(self, date_from: datetime, date_to: datetime) -> [PaystatMonthlyReport]:
        paystats = []
        conn = pg_connection()
        with conn.cursor() as cur:
            cur.execute(f'''
                SELECT p_month::DATE, p_age, p_gender, SUM(amount::FLOAT) 
                FROM paystats
                WHERE p_month BETWEEN '{date_from}' AND '{date_to}'
                GROUP BY p_month, p_age, p_gender
                ORDER BY p_month ASC
            ''')
            paystats = cur.fetchall()
        conn.close()
        return self.get_paystat_list(paystats)

    def get_aggregated_by_time_frame_and_postal_code(self, date_from: datetime, date_to: datetime,
                                                     postal_code: int) -> PaystatMonthlyReport:
        paystats = []
        conn = pg_connection()
        with conn.cursor() as cur:
            cur.execute(f'''
                SELECT p_age, p_gender, SUM(amount::FLOAT) 
                FROM paystats
                WHERE postal_code_id = {postal_code} AND p_month BETWEEN '{date_from}' AND '{date_to}'
                GROUP BY p_age, p_gender
            ''')
            paystats = cur.fetchall()
        conn.close()
        return paystats

    @staticmethod
    def get_paystat_list(paystats: []):
        return [PaystatMonthlyReport(paystat[0], paystat[1], paystat[2], paystat[3]) for paystat in paystats]
