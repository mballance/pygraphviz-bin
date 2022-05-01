'''
Created on Apr 30, 2022

@author: mballance
'''
from unittest.case import TestCase
import graphviz_bin
from _io import StringIO

class TestSmoke(TestCase):
    
    def test_help(self):
        graph = StringIO("""
        digraph {
          A -> B
          B -> A
        }
        """)
        svg = StringIO()
        
        graphviz_bin.dot(["-Tsvg"], graph, svg)
        
        print("Result: %s" % svg.getvalue())