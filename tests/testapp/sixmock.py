try:
    from unittest.mock import patch, Mock, DEFAULT, call  # noqa: F401
except ImportError:
    from mock import patch, Mock, DEFAULT, call  # noqa: F401
