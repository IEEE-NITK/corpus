from corpus.settings import DEBUG

if DEBUG is True:
    raise Exception("DEBUG must be set as False for production.")
