"""The xdist plugin isn't installed so these tests check against the hook contract."""

from unittest import mock

import pytest

from pytest_tap.plugin import TAPPlugin


@pytest.mark.parametrize(
    "combined, stream, expected",
    [
        (False, True, True),
        (True, False, True),
        (False, False, False),
    ],
)
def test_sets_plan_streaming(combined, stream, expected):
    """The plan is set for the given mode conditions by a node's collection report."""
    config = mock.Mock()
    config.option.tap_outdir = "."
    config.option.tap_combined = combined
    config.option.tap_stream = stream
    plugin = TAPPlugin(config)
    node = mock.Mock()
    test_ids = ["a", "b", "c"]

    plugin.pytest_xdist_node_collection_finished(node, test_ids)

    assert (plugin._tracker.plan == 3) is expected
