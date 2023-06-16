import pygame
import pymunk
import sys
import math
from collections import namedtuple

from Engine import Engine

engine = Engine("SuperCoolGame")
engine.engine_config([800,600],"SuperCoolGame",60)

DefaultScene = engine.Scene("DefaultScene", 60, engine.screen)