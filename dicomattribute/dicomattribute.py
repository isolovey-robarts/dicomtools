#!/usr/bin/env python

import pydicom
import argparse

import warnings
from pathlib import Path


class DicomAttribute(object):

    def __init__(self, dicom_file_path, attribute, ignore):
        self._dicom_object = pydicom.dcmread(
            open(dicom_file_path.absolute(), 'rb'),
            stop_before_pixels=True,
        )
        self._attribute = attribute
        self._ignore = ignore

    def process(self):
        if self._attribute is None:
            if self._ignore:
                [delattr(self._dicom_object, i) for i in self._ignore if hasattr(self._dicom_object, i)]
                [delattr(self._dicom_object.file_meta, i) for i in self._ignore if hasattr(self._dicom_object.file_meta, i)]
            print(self._dicom_object.file_meta)
            print(self._dicom_object)
        else:
            for attribute in self._attribute:
                for x in [self._dicom_object, self._dicom_object.file_meta]:
                    if hasattr(x, attribute):
                        print("{0} [{1}]\t\t\t: {2}".format(
                            pydicom.tag.BaseTag(pydicom.datadict.tag_for_name(attribute)).__repr__(),
                            attribute, getattr(x, attribute)))
                        break
                else:
                    warnings.warn("Could not find attribute {0}".format(attribute))


class DicomAttributeArgParser(argparse.ArgumentParser):
    """
        Argument parser for DicomAttribute class

        i.e. argument names of DicomAttributeArgParser match __init__ parameters of DicomAttribute
    """

    def __init__(self):
        super(DicomAttributeArgParser, self).__init__(formatter_class=argparse.RawDescriptionHelpFormatter,
                                                      description='''\
        Dicom attribute extraction
        ''')
        self.add_argument("-a", "--attribute", help="Dicom attribute to display", action='append',
                          default=None)
        self.add_argument("-i", "--ignore", help="Dicom attribute to ignore", action='append',
                          default=None)
        self.add_argument("dicom_file_path", help="Path to Dicom file", type=Path)


if __name__ == "__main__":
    # parse the passed arguments, init and run the pipeline
    args = DicomAttributeArgParser()
    uc = DicomAttribute(**args.parse_args().__dict__)
    uc.process()
