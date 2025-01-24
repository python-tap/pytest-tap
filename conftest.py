import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def sample_test_file(testdir):
    testdir.makepyfile(
        """
        import pytest
        import logging

        LOGGER = logging.getLogger(__name__)

        def test_ok():
            LOGGER.info("Running test_ok")
            assert True

        def test_not_ok():
            LOGGER.error("Running test_not_ok")
            assert False

        @pytest.mark.parametrize('param', ("foo", "bar"))
        def test_params(param):
            assert True

        @pytest.mark.skip(reason='some reason')
        def test_skipped():
            assert False

        @pytest.mark.xfail(reason='a reason')
        def test_broken():
            assert False
    """
    )
