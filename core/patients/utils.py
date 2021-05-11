from collections import namedtuple
from pathlib import Path
from typing import Optional, Union

from django.core.files.storage import default_storage

import pydicom
import rarfile

from dicom_processing.utils import Cut, FileLike, dicom2png, get_slice_cut, open_dcm

GroupedCuts = dict[str, list]


class MRIDecompressManager:
    MAIN_DECOMPRESS_FOLDER = "decompressed"

    def __init__(self, mri) -> None:
        self.mri = mri

    def get_decompression_path(self) -> Path:
        return Path(f"{default_storage.base_location}/{self.MAIN_DECOMPRESS_FOLDER}/{self.mri.pk}/")

    def decompress(self) -> None:
        compressed_file = rarfile.RarFile(self.mri.file.path)
        files_to_extract = (file for file in compressed_file.infolist() if file.filename.lower().endswith(".dcm"))
        compressed_file.extractall(self.get_decompression_path(), files_to_extract)

    def get_files(self, pattern="**/*.dcm"):
        if not self.get_decompression_path().exists():
            self.decompress()

        return self.get_decompression_path().glob(pattern)


class MRIThumbnailsManager:
    MAIN_THUMBNAILS_FOLDER = "file-mris"

    def __init__(self, mri, decompresser: MRIDecompressManager = None):
        # si no se pasa el decompresesr, no se pueden construir las imagenes
        self.mri = mri
        self.decompresser = decompresser

    def get_grouped_images_from_storage(self) -> GroupedCuts:
        grouped_images = self.create_grouped_images_base_structure()

        grouped_images[Cut.Axial].extend(self.get_images_list_from_cut(Cut.Axial))
        grouped_images[Cut.Sagittal].extend(self.get_images_list_from_cut(Cut.Sagittal))
        grouped_images[Cut.Coronal].extend(self.get_images_list_from_cut(Cut.Coronal))

        return grouped_images

    def build_grouped_images(self):
        assert self.decompresser, "Debes establecer un descompresor para poder construir las imagenes"
        images = self.decompresser.get_files()
        grouped_images = self.create_grouped_images_base_structure()

        for file in images:
            data = SingleDicomFileManager.get_cut_and_path(self, file)
            if not data.excluded:
                grouped_images[data.cut_name].append(get_file_url(data.full_path))

        return grouped_images

    def get_mri_path(self):
        return Path(f"{default_storage.base_location}/{self.MAIN_THUMBNAILS_FOLDER}/{self.mri.pk}/")

    def get_cut_path(self, cut: Union[str, Cut]):
        return self.get_mri_path() / str(cut)

    def get_images_list_from_cut(self, cut: Union[str, Cut]):
        return (get_file_url(file) for file in self.get_cut_path(cut).glob("*"))

    @classmethod
    def create_grouped_images_base_structure(cls) -> GroupedCuts:
        return {Cut.Sagittal.value: [], Cut.Coronal.value: [], Cut.Axial.value: [], Cut.Unknown.value: []}


class SingleDicomFileManager:
    DEFAULT_EXCLUDED_DESCRIPTION = "T2 TSE Tra"

    def __init__(self, mri_manager: MRIThumbnailsManager, file: FileLike):
        self.file = file
        self.mri_manager = mri_manager
        self.dcm_dataset: Optional[pydicom.Dataset] = None

    @staticmethod
    def get_cut_and_path(mri_manager, file):
        DicomThumbnailData = namedtuple("DicomThumbnailData", ["cut_name", "full_path", "excluded"])
        dicom_manager = SingleDicomFileManager(mri_manager, file)
        image_thumbnail_path = dicom_manager.build_mri_segmented_thumbnail()
        dcm_cut = dicom_manager.get_cut()
        return DicomThumbnailData(dcm_cut.value, image_thumbnail_path, dicom_manager.should_be_excluded())

    def build_mri_segmented_thumbnail(self, path: Optional[str] = None):
        if self.should_be_excluded():
            return None

        dcm_file = self.get_dataset()
        final_path = path or self.build_mri_slice_path(dcm_file)

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
        return str(self.get_dataset().SeriesDescription).strip() == self.DEFAULT_EXCLUDED_DESCRIPTION

    def get_dataset(self):
        if not self.dcm_dataset:
            self.dcm_dataset = open_dcm(self.file)
        return self.dcm_dataset


def get_file_url(file: Path):
    return default_storage.url(str(file.relative_to(default_storage.base_location)))
