from pathlib import Path
from typing import Optional, Union

from django.core.files.storage import default_storage

import pydicom
from dicom_processing.utils import Cut, FileLike, dicom2png, get_dcm_files_from_rarfile, get_slice_cut, open_dcm


class MRIThumbnailsManager:
    MAIN_FOLDER = "file-mris"

    def __init__(self, mri):
        self.mri = mri

    def get_grouped_images_from_storage(self):
        grouped_images = self.create_grouped_images_base_structure()

        grouped_images[Cut.Axial].extend(self.get_images_list_from_cut(Cut.Axial))
        grouped_images[Cut.Sagittal].extend(self.get_images_list_from_cut(Cut.Sagittal))
        grouped_images[Cut.Coronal].extend(self.get_images_list_from_cut(Cut.Coronal))

        return grouped_images

    async def build_grouped_images(self):
        import timeit

        all_time = timeit.default_timer()
        images = get_dcm_files_from_rarfile(self.mri.file.path)
        grouped_images = self.create_grouped_images_base_structure()

        startime = timeit.default_timer()
        async for dcm_open_file in images:
            print(timeit.default_timer() - startime)
            startime = timeit.default_timer()
            dicom_file = SingleDicomFileManager(self, dcm_open_file)

            if dicom_file.should_be_excluded():
                continue

            image_thumbnail_path = await dicom_file.async_build_mri_segmented_thumbnail(dcm_open_file)
            dcm_cut = dicom_file.get_cut()
            grouped_images[dcm_cut.value].append(get_file_url(image_thumbnail_path))

        print("final time:", timeit.default_timer() - all_time)

        return grouped_images

    def get_mri_path(self):
        return Path(f"{default_storage.base_location}/{self.MAIN_FOLDER}/{self.mri.pk}/")

    def get_cut_path(self, cut: Union[str, Cut]):
        return self.get_mri_path() / str(cut)

    def get_images_list_from_cut(self, cut: Union[str, Cut]):
        return (get_file_url(file) for file in self.get_cut_path(cut).glob("*"))

    @classmethod
    def create_grouped_images_base_structure(cls):
        return {Cut.Sagittal.value: [], Cut.Coronal.value: [], Cut.Axial.value: [], Cut.Unknown.value: []}


class SingleDicomFileManager:
    DEFAULT_EXCLUDED_DESCRIPTION = "T2 TSE Tra"

    def __init__(self, mri_manager: MRIThumbnailsManager, file: FileLike):
        self.mri_manager = mri_manager
        self.file = file
        self.dcm_dataset: Optional[pydicom.Dataset] = None

    def get_cut(self) -> Cut:
        return get_slice_cut(self.get_dataset())

    def build_mri_segmented_thumbnail(self, file: FileLike):
        dcm_file = self.get_dataset()
        final_path = self.build_mri_slice_path(dcm_file)

        if not default_storage.exists(final_path):
            dicom2png(dcm_file, str(final_path))

        return final_path

    async def async_build_mri_segmented_thumbnail(self, file: FileLike):
        return self.build_mri_segmented_thumbnail(file)

    def build_mri_slice_path(self, dcm: pydicom.Dataset) -> Path:
        cut_name = get_slice_cut(self.get_dataset())
        return self.mri_manager.get_cut_path(cut_name) / f"{dcm.SOPInstanceUID}.png"

    def should_be_excluded(self):
        # annadir aqui mas condiciones si en el futuro se requieren
        return self.get_dataset().SeriesDescription == self.DEFAULT_EXCLUDED_DESCRIPTION

    def get_dataset(self):
        if not self.dcm_dataset:
            self.dcm_dataset = open_dcm(self.file)
        return self.dcm_dataset


def get_file_url(file: Path):
    return default_storage.url(str(file.relative_to(default_storage.base_location)))
