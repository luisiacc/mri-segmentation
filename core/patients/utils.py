from pathlib import Path
from typing import Iterable, Union

from django.core.files.storage import default_storage

import pydicom
from dicom_processing.utils import Cut, FileLike, dicom2png, get_dcm_files_from_rarfile, get_slice_cut, open_dcm


class MRIThumbnailBuilder:
    MAIN_FOLDER = "file-mris"

    def __init__(self, mri):
        self.mri = mri

    def get_grouped_images_from_storage(self):
        grouped_images = self.create_grouped_images_base_structure()

        grouped_images[Cut.Axial].extend(self.get_images_list_from_cut(Cut.Axial.value))
        grouped_images[Cut.Sagittal].extend(self.get_images_list_from_cut(Cut.Sagittal.value))
        grouped_images[Cut.Coronal].extend(self.get_images_list_from_cut(Cut.Coronal.value))

        return grouped_images

    def construct_grouped_images(self):
        import timeit

        images: Iterable[FileLike] = get_dcm_files_from_rarfile(self.mri.file.path)
        grouped_images = self.create_grouped_images_base_structure()

        startime = timeit.default_timer()
        for dcm_open_file in images:
            print(timeit.default_timer() - startime)
            startime = timeit.default_timer()
            image_thumbnail_path = build_mri_segmented_thumbnail(self.mri, dcm_open_file)
            dcm_cut: Cut = get_slice_cut(dcm_open_file)
            grouped_images[dcm_cut.value].append(image_thumbnail_path)

        return grouped_images

    def get_mri_path(self):
        return Path(f"{default_storage.base_location}/{self.MAIN_FOLDER}/{self.mri.pk}/")

    def get_cut_path(self, cut: Union[str, Cut]):
        return self.get_mri_path() / str(cut)

    def get_images_list_from_cut(self, cut: Union[str, Cut]):
        def get_relative_path(file):
            return default_storage.url(str(file.relative_to(default_storage.base_location)))

        return (get_relative_path(file) for file in self.get_cut_path(cut).glob("*"))

    @classmethod
    def create_grouped_images_base_structure(cls):
        return {Cut.Sagittal.value: [], Cut.Coronal.value: [], Cut.Axial.value: [], Cut.Unknown.value: []}


def build_mri_cut_path(mri, dcm: pydicom.Dataset) -> Path:
    cut_name = get_slice_cut(dcm)
    return Path(f"./file-mris/{mri.pk}/{cut_name}/{dcm.SOPInstanceUID}.png")


def build_mri_segmented_thumbnail(mri, file: FileLike):
    dcm_file = open_dcm(file)
    final_path = build_mri_cut_path(mri, dcm_file)

    if not default_storage.exists(final_path):
        dicom2png(file, str(final_path))

    return str(final_path)


async def async_build_mri_segmented_thumbnail(mri, file: FileLike):
    return build_mri_segmented_thumbnail(mri, file)
