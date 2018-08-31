 Dicomtools
 ----------
 
 - `dicomattribute` - display header attributes of a DICOM file (see
   `dicomattribute -h`)
 
 - `dicomdiff` - apply `dicomattribute` to two dicom files and diff the
   outputs using system `diff`. (usage: `dicomdiff file1 file2`).


Installation
============

1. Create a virtual environment with `virtualenv`/`virtualenvwrapper` and install dependencies:

```
mkvirtualenv -p python3 -a . dicomtools
pip install -r requirements.txt
```

2. Put the bash scripts on your PATH. One of:

 - `ln -s dicomattribute/dicomattribute /somewhere/on/my/system/path/dicomattribute && ln -s dicomdiff/dicomdiff /somewhere/on/my/system/path/dicomdiff`
 
 or
 

 - `export PATH=${PATH}:${pwd}/dicomattribute:${pwd}/dicomdiff`
