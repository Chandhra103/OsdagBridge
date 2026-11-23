import pytest

pytest.importorskip("openseespy.opensees", reason="OpenSeesPy is required by the design module")

from osdagbridge.core.bridge_types.plate_girder.designer import DCREngine
from osdagbridge.core.utils.codes.keyfile import DCR_FAIL_THRESHOLD, DCR_PASS_THRESHOLD


@pytest.mark.parametrize(
    ("dcr", "expected"),
    [
        (0.0, "PASS"),
        (DCR_PASS_THRESHOLD - 1e-12, "PASS"),
        (DCR_PASS_THRESHOLD, "WARN"),
        (DCR_FAIL_THRESHOLD - 1e-12, "WARN"),
        (DCR_FAIL_THRESHOLD, "FAIL"),
        (DCR_FAIL_THRESHOLD + 0.5, "FAIL"),
    ],
)
def test_dcr_classification_respects_configured_boundaries(dcr, expected):
    assert DCREngine.classify(dcr) == expected
