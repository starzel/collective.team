from mock import Mock
import unittest2 as unittest

class TestJSON(unittest.TestCase):
    def testSomeTree(self):
        from collective.team.browser.team import JSONView
        from json import loads
        view = JSONView(None, None)
        view.context = Mock()
        view.context.getPhysicalPath = lambda: []
        view.site = Mock()
        results = [Mock(), Mock(), Mock(), Mock()]
        results[0].getPath = lambda: '/path1'
        results[0].Title = 'Path 1'
        results[1].getPath = lambda: '/path1/path1.1'
        results[1].Title = 'Path 1.1'
        results[2].getPath = lambda: '/path1/path1.1/path1.1.1'
        results[2].Title = 'Path 1.1.1'
        results[3].getPath = lambda: '/path2'
        results[3].Title = 'Path 2'
        view.site.portal_catalog.return_value = results
        expected = [{"key": "/path1",
                     "isFolder": True,
                     "children": [{"key": "/path1/path1.1",
                                   "isFolder": True,
                                   "children": [{"key":
                                                     "/path1/path1.1/path1.1.1",
                                                 "isFolder": True,
                                                 "children": [],
                                                 "title": "Path 1.1.1"}],
                                   "title": "Path 1.1"}],
                     "title": "Path 1"},
                    {"key": "/path2",
                     "isFolder": True,
                     "children": [],
                     "title": "Path 2"}]
        self.assertEquals(expected, loads(view()))
