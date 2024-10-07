import os
from dataclasses import dataclass

@dataclass
class Element:
    # name: str
    relPath: str
    # size: int

@dataclass
class File(Element):
    # fileSize: int
    # fileType: str
    pass

@dataclass
class Directory(Element):
    children: list

elements = []

root = "./testfolder"
for element in os.listdir(root):
    print(element)
    element_path = root + "\\" + element
    # print(element_path)
    if os.path.isdir(element_path):
        for element in os.listdir(element_path):
            print("     " + element) 