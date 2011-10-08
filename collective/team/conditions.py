from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from zope.site.hooks import getSite

class WithinTeamAreaAndNotManager(object):
    """ test if the user is a plone-manager"""
    def __init__(self, context, request):
        """ test"""
        self.request = request
        self.context = context

    def __call__(self):
        """ test"""
        if 'wissen/intranet/special-interest-groups' in self.request.ACTUAL_URL:
            portal = getSite()
            if self.sec_manager.checkPermission(permissions.ManagePortal,
                                                portal):
                return False
            return True
        else:
            return False

    @property
    def sec_manager(self):
        if not hasattr(self, '_sec_manager'):
            self._sec_manager = getSecurityManager() # pragma: no cover
        return self._sec_manager


class WithinTeamArea(object):
    """ check if we are within the team-area """

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self):
        if 'wissen/intranet/special-interest-groups' in self.request.ACTUAL_URL:
            return True
        else:
            return False

