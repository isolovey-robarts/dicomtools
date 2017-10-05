#!/usr/bin/env python
import difflib

import dicom
import argparse

import warnings


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    source: http://stackoverflow.com/questions/1165352/calculate-difference-in-keys-contained-in-two-python-dictionaries
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


class DicomDiff(object):

    def __init__(self, dicom_file_1_path, dicom_file_2_path):
        self._dicom_objects = (
            dicom.read_file(dicom_file_1_path, stop_before_pixels=True, force=True),
            dicom.read_file(dicom_file_2_path, stop_before_pixels=True, force=True)
        )

    def process(self):

        rep = []
        for dataset in self._dicom_objects:
            lines = str(dataset).split("\n")
            lines = [line for line in lines]  # add the newline to end
            rep.append(lines)

        diff = difflib.Differ()
        print '\n'
        for line in diff.compare(rep[0], rep[1]):
            if line[0] == "+" or line[0] == '-':
                print(line)

class DicomDiffArgParser(argparse.ArgumentParser):
    """
        Argument parser for DicomDiff class

        i.e. argument names of DicomDiffArgParser match __init__ parameters of DicomDiff
    """

    def __init__(self):
        super(DicomDiffArgParser, self).__init__(formatter_class=argparse.RawDescriptionHelpFormatter,
                                                 description='''\
        Print diff between two dicom file headers
        ''')
        self.add_argument("dicom_file_1_path", help="Path to Dicom file 1", type=argparse.FileType('r'))
        self.add_argument("dicom_file_2_path", help="Path to Dicom file 2", type=argparse.FileType('r'))

if __name__ == "__main__":
    # parse the passed arguments, init and run the pipeline
    args = DicomDiffArgParser()
    uc = DicomDiff(**args.parse_args().__dict__)
    uc.process()
