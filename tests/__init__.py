import os
import sys
TEST_ROOT_DIR = os.path.dirname(__file__)
parentdir = os.path.dirname(TEST_ROOT_DIR)
parentdir2 = os.path.dirname(TEST_ROOT_DIR)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir2)
os.chdir(TEST_ROOT_DIR)
