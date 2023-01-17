class BaseBotError(Exception):
    def __init__(self, chat_id, message):
        super().__init__(message)
        self.chat_id = chat_id


class NonExistentParticipantError(BaseBotError):
    pass


class NotAdminError(BaseBotError):
    pass


class NotEnoughQuestionsError(BaseBotError):
    pass


class CouldNotCreateQuestions(BaseBotError):
    pass


class WrongFileExtensionError(BaseBotError):
    pass