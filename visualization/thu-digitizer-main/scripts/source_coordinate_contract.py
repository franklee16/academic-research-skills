"""Identity and coordinate-space contract for original raster measurements."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image


ORIGINAL_RASTER_SPACE = "original_raster_pixels"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class RasterIdentity:
    sha256: str
    width: int
    height: int
    coordinate_space: str = ORIGINAL_RASTER_SPACE

    def as_dict(self) -> dict[str, Any]:
        return {
            "sha256": self.sha256,
            "width": self.width,
            "height": self.height,
            "coordinate_space": self.coordinate_space,
            "resampling_applied": False,
        }


def raster_identity(path: Path) -> RasterIdentity:
    with Image.open(path) as image:
        width, height = image.size
    return RasterIdentity(sha256=file_sha256(path), width=width, height=height)


def assert_original_raster(path: Path, expected: dict[str, Any]) -> RasterIdentity:
    """Reject a preview, resized copy, or different encoding before measurement."""

    actual = raster_identity(path)
    if expected.get("coordinate_space") != ORIGINAL_RASTER_SPACE:
        raise ValueError(
            f"source.coordinate_space must equal {ORIGINAL_RASTER_SPACE!r}"
        )
    mismatches = []
    if expected.get("sha256") != actual.sha256:
        mismatches.append("sha256")
    if expected.get("width") != actual.width:
        mismatches.append("width")
    if expected.get("height") != actual.height:
        mismatches.append("height")
    if mismatches:
        raise ValueError(
            "input does not match the original-raster contract "
            f"({', '.join(mismatches)} mismatch); do not measure a preview, "
            "thumbnail, screenshot, or resized copy"
        )
    return actual
