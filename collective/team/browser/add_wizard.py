from Products.Five.browser import BrowserView
from json import dumps

class AddWizard(BrowserView):
    """ An enhanced add view
    """
    def __call__(self):
        if 'folder' in self.request.form:
            return self.subfolders(self.request.form['folder'])
        else:
            return self.index()

    @property
    def additional_folders(self):
        retval = []
        for obj in self.context.getFolderContents(
            {'portal_type' : 'Folder'}):
            if obj.id not in ['bilder', 'dokumente', 'termine']:
                retval.append({'key': obj.id,
                               'value': obj.Title})
        return retval

    def subfolders(self, folder):
        retval = []
        for obj in self.context[folder].getFolderContents():
            retval.append({'key': obj.id,
                           'value': obj.Title})
        self.request.response.setHeader("Content-type", "text/json")
        return dumps(retval)
