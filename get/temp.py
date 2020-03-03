import os, tempfile

dirpath = tempfile.mkdtemp()
print('**************************')
print(dirpath)
print(os.path.dirname(dirpath))
print(os.path.basename(dirpath))
