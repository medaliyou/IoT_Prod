S_KEY = S_RANDOM_NUMBER = S_RANDOM_NONCE = S_PASSWORD = S_ID = 16  # 16 Bytes <=> 128 bits


class ErrorModel(Exception):
    err_no: int
    err_message: str

    def __init__(self, err_no: int = None, err_message: str = None):
        if err_no is not None:
            self.err_no = err_no
        if err_message is not None:
            self.err_message = err_message

    def __str__(self):
        return self.err_message
