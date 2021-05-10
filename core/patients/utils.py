import asyncio
from collections import namedtuple
from concurrent.futures.thread import ThreadPoolExecutor
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

        init_time = timeit.default_timer()
        images = get_dcm_files_from_rarfile(self.mri.file.path)
        grouped_images = self.create_grouped_images_base_structure()

        async def run_operation(file):
            data = await SingleDicomFileManager.get_cut_and_path(self, file)
            if not data.excluded:
                grouped_images[data.cut_name].append(get_file_url(data.full_path))

        await asyncio.gather(*[run_operation(file) for file in images])

        print("final time:", timeit.default_timer() - init_time)

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
    executor = ThreadPoolExecutor(5)

    def __init__(self, mri_manager: MRIThumbnailsManager, file: FileLike):
        self.mri_manager = mri_manager
        self.file = file
        self.dcm_dataset: Optional[pydicom.Dataset] = None

    @staticmethod
    async def get_cut_and_path(mri_manager, file):
        DicomThumbnailData = namedtuple("DicomThumbnailData", ["cut_name", "full_path", "excluded"])
        dicom_file = SingleDicomFileManager(mri_manager, file)
        image_thumbnail_path = await dicom_file.build_mri_segmented_thumbnail()
        dcm_cut = dicom_file.get_cut()
        return DicomThumbnailData(dcm_cut.value, image_thumbnail_path, dicom_file.should_be_excluded())

    async def build_mri_segmented_thumbnail(self):
        dcm_file = await self.async_get_dataset()
        final_path = self.build_mri_slice_path(dcm_file)

        if not default_storage.exists(final_path):
            dicom2png(dcm_file, str(final_path))

        return final_path

    def get_cut(self) -> Cut:
        return get_slice_cut(self.get_dataset())

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

    async def async_get_dataset(self):
        loop = asyncio.get_event_loop()
        if not self.dcm_dataset:
            self.dcm_dataset = await loop.run_in_executor(self.executor, open_dcm, self.file)
        return self.dcm_dataset


def get_file_url(file: Path):
    return default_storage.url(str(file.relative_to(default_storage.base_location)))
