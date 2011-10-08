from five import grok
from plone.app.layout.viewlets import interfaces as viewletIFs
from zope.app.component.hooks import getSite
from zope.interface import Interface
from Products.CMFCore.permissions import ModifyPortalContent, AddPortalContent 
from AccessControl import getSecurityManager

from collective.team.behaviors.team import ITeam

class Intranet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(viewletIFs.IAboveContent)

    @property
    def available(self):
        is_team = False
        is_folder = False
        is_in_sig = False
        is_in_team = False
        edit_content = False
        add_content = False
        list_content = False
        if 'special-interest-groups' in self.context.getPhysicalPath():
            is_in_sig = True
            teams = filter(ITeam.providedBy, self.request.PARENTS)
            if ITeam.providedBy(self.context):
                is_team = True
            if self.context.portal_type == 'Folder':
                is_folder = True
            if teams:
                is_in_team = True
                self.team = teams[0]
            
            sm = getSecurityManager()
            if sm.checkPermission(ModifyPortalContent, self.context):
                edit_content = True
            if sm.checkPermission(AddPortalContent, self.context):
                add_content = True
        retval = {
            'add_wizard' : is_in_team and add_content,
            'mail_to_member' : is_in_team and not (is_team or is_folder),
            'manage_content' : is_in_team and edit_content,
            'edit' : is_in_team and edit_content,
            }
        return retval

    @property
    def users(self):
        retval = []
        if not hasattr(self, 'site'):
            self.site = getSite()
        for member in self.team.managers +\
                [x for x in self.team.members if x not in self.team.managers]:
            pmember = self.site.acl_users.getUserById(member)
            if pmember:
                retval.append({'email' : pmember.getProperty("email"),
                               'id' : pmember.getName()})
        return retval
