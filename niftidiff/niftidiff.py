#!/usr/bin/env python

import nibabel
import numpy as np
from deepdiff import DeepDiff
import argparse

from pathlib import Path

from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style

class DicomAttribute(object):

    def __init__(self, nifti_file_1, nifti_file_2):
        self._I1 = nibabel.load(str(nifti_file_1))
        self._I2 = nibabel.load(str(nifti_file_2))

    def process(self):
        h1 = self._I1.header
        h2 = self._I2.header
        d1 = self._I1.get_data()
        d2 = self._I2.get_data()
        ddiff = DeepDiff(h1.__str__(), h2.__str__(), ignore_order=True)
        print('---Header---')
        print(ddiff.get('values_changed', {}).get('root', {}).get('diff', '-----NONE-----'))
        print('---Data---')
        dims_eq = np.all(d1.shape == d2.shape)
        print('dimensions equal? {}'.format(dims_eq))
        numel_eq = np.size(d1) == np.size(d2)
        print('number of elements equal? {}'.format(numel_eq))
        if numel_eq:
            d1 = d1.flatten()
            d2 = d2.flatten()
            elems_eq = np.all(d1 == d2)
            print('all elements equal? {}'.format(colored(Fore.REDelems_eq))
            diff = np.subtract(d1, d2)
            nz = np.logical_and(
                d1 != 0,
                d2 != 0
            )
            print('diff: {:.4f}%'.format(np.sum(np.abs(diff[nz]))/np.sum(d1[nz])*100.0))


class DicomAttributeArgParser(argparse.ArgumentParser):
    """
        Argument parser for DicomAttribute class

        i.e. argument names of DicomAttributeArgParser match __init__ parameters of DicomAttribute
    """

    def __init__(self):
        super(DicomAttributeArgParser, self).__init__(formatter_class=argparse.RawDescriptionHelpFormatter,
                                                      description='''\
        Nifti diff
        ''')
        self.add_argument("nifti_file_1", help="Nifti file 1", type=Path)
        self.add_argument("nifti_file_2", help="Nifti file 2", type=Path)


if __name__ == "__main__":
    # parse the passed arguments, init and run the pipeline
    args = DicomAttributeArgParser()
    uc = DicomAttribute(**args.parse_args().__dict__)
    uc.process()
