from domain.repository.PostalCodeRepository import PostalCodeRepository


class PostalCodeService:
    def __init__(self, repository: PostalCodeRepository):
        self.repository = repository

    def get_all(self, date_from, date_to):
        return self.repository.find_all_by_time_frame(date_from, date_to)

    def get_by_did(self, did, date_from, date_to):
        return self.repository.find_by_did_and_time_frame(did, date_from, date_to)
