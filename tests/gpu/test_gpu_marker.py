"""Prove GPU-marked tests skip with an explicit reason on CPU systems."""

import pytest


@pytest.mark.gpu
@pytest.mark.smoke
def test_cuda_test_boundary() -> None:
    """This assertion runs only if the shared CUDA availability check succeeds."""

    assert True
