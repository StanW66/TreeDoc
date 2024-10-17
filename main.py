import os
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import re

### GLOBAL VARIABLES ###
PROJECT_FOLDER = "."
START_X, START_Y = 10, 10
LINE_NUMBER = 1
ELEMENT_LIST = [] 
FONT_SIZE = 30
ICON_SIZE = FONT_SIZE 
PARENT_OFFSET_Y = FONT_SIZE + 5
PARENT_OFFSET_X = ICON_SIZE / 2
CHILD_OFFSET_Y = FONT_SIZE / 2
CHILD_OFFSET_X = -5
LINE_INCREMENT = FONT_SIZE + 10
DEPTH_INCREMENT = 50
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000
ICON_DIR = "./icons/"

### CLASSES ###
@dataclass
class Element:
    relPath: str
    name: str
    xy: tuple
    def __eq__(self, other) -> bool:
        return self.xy[1] == other.xy[1]
    def __lt__(self, other) -> bool:
        return self.xy[1] < other.xy[1]
    def __gt__(self, other) -> bool:
        return self.xy[1] > other.xy[1]

@dataclass
class File(Element):
    def get_file_suffix(self) -> str: # thanks gpt
        match = re.search(r'\.([^.]+)$', self.name)
        return match.group(1) if match else "generic"
    def define_element_icon(self) -> str:
        icon = self.get_file_suffix() + ".png"
        if icon not in os.listdir(ICON_DIR):
            icon = "generic.png"
        return ICON_DIR + icon

@dataclass
class Directory(Element):
    children: list
    def define_element_icon(self) -> str:
        if len(self.children) > 0:
            icon = "full_dir.png"
        else: 
            icon = "empty_dir.png"
        return ICON_DIR + icon

### FUNCTIONS ###
def load_ignores() -> list:
    dir_list = os.listdir(PROJECT_FOLDER)
    if ".tdignore" in dir_list:
        with open(".tdignore","r") as tdi:
            ignore_list = list(map(lambda x: x.strip(), tdi.readlines()))
    else:
        print("no ignore file found.")
    return ignore_list

def check_igonre(element_path) -> bool:
    if element_path[2:] in IGNORE_LIST:
        return True
    else:
        return False

def tree_walker(path, depth) -> list:
    global LINE_NUMBER, ELEMENT_LIST
    objects = []
    elements = os.listdir(path)
    for element in elements:
        element_path = path + "/" + element
        if check_igonre(element_path):
            continue
        LINE_NUMBER += 1
        x, y = depth * DEPTH_INCREMENT, LINE_NUMBER * LINE_INCREMENT
        if os.path.isdir(element_path):
            children = tree_walker(element_path, depth+1)
            obj = Directory(element_path, element, (x,y), children)
            objects.append(obj)
            ELEMENT_LIST.append(obj)
        else:
            obj = File(element_path, element, (x,y))
            objects.append(obj)
            ELEMENT_LIST.append(obj)
    return objects

def get_text_dimensions(text_string, font) -> tuple:
    # source: https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent + ascent
    return (text_width, text_height)

def define_window_size():
    global WINDOW_WIDTH, WINDOW_HEIGHT, LINE_INCREMENT
    max = 0
    for element in ELEMENT_LIST:
        text_width, text_height = get_text_dimensions(element.name, font=font)
        length = text_width + element.xy[0]
        if length > max:
            max = length 
    WINDOW_WIDTH = max + START_X*4 + ICON_SIZE
    WINDOW_HEIGHT = len(ELEMENT_LIST) * LINE_INCREMENT + 3 * LINE_INCREMENT
    return

def build_tree(path):
    elements = tree_walker(path, 1)
    define_window_size()
    return 

def print_text():
    for element in sorted(ELEMENT_LIST):
        xy = (element.xy[0] + ICON_SIZE + 5, element.xy[1])
        draw.text(xy=(xy), text=element.name, fill="black", font=font)
    return 

def print_branches(): # fix ofset to make space for the icons
    for element in ELEMENT_LIST:
        if type(element) == Directory:
            parent_xy = (element.xy[0] + PARENT_OFFSET_X, element.xy[1] + PARENT_OFFSET_Y)
            for child in element.children:
                child_xy = (child.xy[0] + CHILD_OFFSET_X, child.xy[1] + CHILD_OFFSET_Y)
                elbow = (parent_xy[0], child_xy[1])
                draw.line([parent_xy, elbow], fill="black", width=1)
                draw.line([child_xy, elbow], fill="black", width=1)
    return

def print_icons():
    for element in ELEMENT_LIST:
        icon_path = element.define_element_icon()
        with Image.open(icon_path) as i:
            smol_icon = i.resize((ICON_SIZE,ICON_SIZE))
            image.paste(smol_icon, element.xy, smol_icon)
    return

def print_project_name(): # this is not working
    project_name = os.path.basename(os.getcwd())
    draw.text(xy=(START_X,START_Y), text=project_name, fill="black", font=title_font)
    return

def printer(): 
    print_project_name()
    print_icons()
    print_text()
    print_branches()
    return

### TEST ### 
font = ImageFont.load_default(size=FONT_SIZE)
title_font = ImageFont.load_default(size=int(FONT_SIZE * 1.5))
# build the tree
IGNORE_LIST = load_ignores()
build_tree(PROJECT_FOLDER)
# initialize iamgedrawer object
image = Image.new("RGB", (WINDOW_WIDTH, WINDOW_HEIGHT), "white")
draw = ImageDraw.Draw(image)

# draw the tree into the image
printer()

image.save("example.png")