from datetime import datetime
from util.date import get_date_frame
from . import app, cache
from flask_jwt_extended import verify_jwt_in_request

from adapter.repository.PaystatMonthlyReportRepositoryPostgres import PaystatMonthlyReportRepositoryPostgres
from domain.service.PaystatMonthlyReportService import PaystatMonthlyReportService
from flask.views import MethodView
from adapter.repository.PostalCodeRepositoryPostgres import PostalCodeRepositoryPostgres
from domain.service.PostalCodeService import PostalCodeService
from flask import jsonify, request, abort


class PostalCodeResource(MethodView):
    def __init__(self):
        verify_jwt_in_request()
        self.repository = PostalCodeRepositoryPostgres()
        self.service = PostalCodeService(self.repository)

    @cache.cached(timeout=50, query_string=True)
    def get(self, did):
        try:
            date_from, date_to = get_date_frame(request.args.get('date_from', None), request.args.get('date_to', None))
        except ValueError:
            abort(400)

        if did is None:
            postal_codes = self.service.get_all(date_from, date_to)
            return jsonify([vars(postal_code) for postal_code in postal_codes])
        else:
            postal_code = self.service.get_by_did(did, date_from, date_to)
            if postal_code is None:
                abort(404)
            return jsonify(vars(postal_code))


class PostalCodePaystatResource(MethodView):
    def __init__(self):
        self.repository = PaystatMonthlyReportRepositoryPostgres()
        self.service = PaystatMonthlyReportService(self.repository)

    @cache.cached(timeout=50, query_string=True)
    def get(self, did):
        try:
            date_from, date_to = get_date_frame(request.args.get('date_from', None), request.args.get('date_to', None))
        except ValueError:
            abort(400)

        paystat_aggregates = {}

        paystat_monthly_aggregates = self.service.get_aggregated_by_time_frame_and_postal_code(date_from, date_to, did)
        for row in paystat_monthly_aggregates:
            paystat_aggregates.setdefault(row[0], {}).update({row[1]: row[2]})

        return jsonify(paystat_aggregates)


postal_code_resource = PostalCodeResource.as_view('postal_code_resource')
app.add_url_rule('/postal_code/', defaults={'did': None}, view_func=postal_code_resource, methods=['GET', ])

# Add a subresource URL to get paystat aggregates for a postal code
postal_code_paystat_resource = PostalCodePaystatResource.as_view('postal_code_paystat_resource')
app.add_url_rule('/postal_code/<int:did>/paystat_aggregate', view_func=postal_code_paystat_resource, methods=['GET', ])
