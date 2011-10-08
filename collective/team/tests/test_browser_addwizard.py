import unittest2 as unittest
from mock import Mock

class TestAddWizard(unittest.TestCase):
    def test_call_does_nothing(self):
        from collective.team.browser.add_wizard import AddWizard
        request = Mock()
        request.form = {}
        view = AddWizard(None, request)
        view.index = Mock()
        view()
        self.assertEquals(1, view.index.call_count)

    def test_call_returns_subfolders(self):
        from collective.team.browser.add_wizard import AddWizard
        request = Mock()
        request.form = {'folder' : 'folder1'}
        folder = Mock()
        folder.getFolderContents = lambda: []
        context = {'folder1' : folder}
        view = AddWizard(context, request)
        self.assertEquals('[]', view())

    def test_additional_folders(self):
        """
        Additional folders ignores some folders, like bilder
        """
        from collective.team.browser.add_wizard import AddWizard
        view = AddWizard(None, None)
        view.context = Mock()
        folders = [Mock(), Mock()]
        view.context.getFolderContents = lambda x: folders
        folders[0].id = 'bilder'
        folders[1].id = 'folder1'
        folders[1].Title = 'Title1'
        self.assertEquals([{'value': 'Title1', 'key': 'folder1'}],
                          view.additional_folders)

    def test_subfolders(self):
        from collective.team.browser.add_wizard import AddWizard
        view = AddWizard(None, None)
        view.context = {'folder1' : Mock()}
        view.request = Mock()
        folders = [Mock()]
        view.context['folder1'].getFolderContents = lambda: folders
        folders[0].id = 'folder2'
        folders[0].Title = 'Title2'
        self.assertEquals('[{"value": "Title2", "key": "folder2"}]',
                          view.subfolders('folder1'))
