from io import BytesIO, FileIO
from typing import BinaryIO, Union

from django.core.files.storage import default_storage
from django.db.models.enums import TextChoices

import numpy as np
import png

import pydicom
import rarfile

DEFAULT_EXCLUDED_CUT = "T2 TSE Tra"

FileLike = Union[BytesIO, BinaryIO, FileIO, rarfile.PipeReader, rarfile.DirectReader]


class Cut(TextChoices):
    Sagittal = "sagittal"
    Coronal = "coronal"
    Axial = "axial"
    Unknown = "unkown"


def open_dcm(file: Union[str, FileLike], *args, **kwargs):
    if isinstance(file, FileLike.__args__):
        file.seek(0)

    return pydicom.dcmread(file, *args, **kwargs)


def dicom2png(source_file: Union[str, FileLike, pydicom.Dataset], output_file: str):
    if isinstance(source_file, pydicom.Dataset):
        ds = source_file
    else:
        ds = open_dcm(source_file)

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    new_file_stream = BytesIO()
    w = png.Writer(shape[1], shape[0], greyscale=True)
    w.write(new_file_stream, image_2d_scaled)
    default_storage.save(output_file, new_file_stream)


def get_slice_cut(dcm: pydicom.Dataset) -> Cut:
    IOP: list = getattr(dcm, "ImageOrientationPatient", [])
    assert len(IOP), "ImageOrientationPatient no puede ser una lista vacia"

    IOP_round = [round(x) for x in IOP]
    plane = np.cross(IOP_round[0:3], IOP_round[3:6])
    plane = [abs(x) for x in plane]

    if plane[0] == 1:
        return Cut.Sagittal
    elif plane[1] == 1:
        return Cut.Coronal
    elif plane[2] == 1:
        return Cut.Axial

    return Cut.Unknown
