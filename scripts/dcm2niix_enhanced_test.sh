#!/usr/bin/env bash

DICOM_DATASET=${1}
#rm -rf /tmp/dcm2niix_enhanced_test*
WORKDIR=$(mktemp -d --tmpdir dcm2niix_enhanced_testXXXXX)

if [ -f "${DICOM_DATASET}" ]; then
    tar tf ${DICOM_DATASET} > /dev/null 2>&1 || { echo "Invalid file (needs to be a valid tarball)"; exit 1; }
    cd ${WORKDIR}
    mkdir -p dicom
    cd dicom
    tar --transform 's/.*\///g' -xvf ${DICOM_DATASET}
elif [ -d "${DICOM_DATASET}" ]; then
    ln -s ${DICOM_DATASET} ${WORKDIR}/dicom
else
   echo "Invalid dicom source ${1}" && exit 1
fi

cd ${WORKDIR}
mkdir -p ${WORKDIR}/nifti/unenh
dcm2niix_bruker ${WORKDIR}/dicom ${WORKDIR}/nifti/unenh
mkdir -p ${WORKDIR}/nifti/enh
dcm2niix -d 9 -o ${WORKDIR}/nifti/enh ${WORKDIR}/dicom


SERIES_LIST=$(ls --color=no ${WORKDIR}/nifti/enh/*.nii|cut -d'.' -f1|rev|cut -d_ -f1|rev)

for f in ${SERIES_LIST}; do
    echo ---START $f----
    niftidiff nifti/enh/*_${f}.nii* nifti/unenh/*_${f}.nii*
    echo ---END $f ----
done
