from util.date import get_date_frame
from . import app, cache
from flask.views import MethodView
from flask import jsonify, request, abort
from adapter.repository.PaystatMonthlyReportRepositoryPostgres import PaystatMonthlyReportRepositoryPostgres
from domain.service.PaystatMonthlyReportService import PaystatMonthlyReportService
from flask_jwt_extended import verify_jwt_in_request


class PaystatMonthlyReportResource(MethodView):
    def __init__(self):
        verify_jwt_in_request()
        self.repository = PaystatMonthlyReportRepositoryPostgres()
        self.service = PaystatMonthlyReportService(self.repository)

    @cache.cached(timeout=50, query_string=True)
    def get(self):
        try:
            date_from, date_to = get_date_frame(request.args.get('date_from', None), request.args.get('date_to', None))
        except ValueError:
            abort(400)

        paystat_monthly_reports = self.service.get_by_time_frame(date_from, date_to)
        return jsonify(PaystatMonthlyReportResource.get_paystat_list(paystat_monthly_reports))

    @staticmethod
    def get_paystat_list(paystat_monthly_reports):
        return [vars(paystat_monthly_report) for paystat_monthly_report in paystat_monthly_reports]


paystat_monthly_report_resource = PaystatMonthlyReportResource.as_view('paystat_monthly_report_resource')
app.add_url_rule('/paystat_monthly_report', view_func=paystat_monthly_report_resource, methods=['GET', ])
