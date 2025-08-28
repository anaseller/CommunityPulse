class CustomBaseException(Exception):

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class EntityNotFoundException(CustomBaseException):
    pass


class DatabaseException(CustomBaseException):
    pass


class PollNotFoundException(CustomBaseException):
    pass


class PollValidationException(CustomBaseException):
    pass


class PollDatabaseException(CustomBaseException):
    pass


class PollCreationException(CustomBaseException):
    pass


class PollUpdateException(CustomBaseException):
    pass


class PollDeletionException(CustomBaseException):
    pass


class VoteNotFoundException(CustomBaseException):
    pass


class VoteValidationException(CustomBaseException):
    pass


class VoteDatabaseException(CustomBaseException):
    pass


class VoteCreationException(CustomBaseException):
    pass


class VoteUpdateException(CustomBaseException):
    pass


class VoteDeletionException(CustomBaseException):
    pass