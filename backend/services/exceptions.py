class CaptchaRequiredError(Exception):
    def __int__(self, url: str=None):
        self.message = 'Требуется ввод капчи'
        self.url = url