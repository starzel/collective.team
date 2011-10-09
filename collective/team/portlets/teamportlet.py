from zope import schema
from zope.component import getMultiAdapter #@UnresolvedImport
from zope.formlib import form
from zope.interface import implements

from Acquisition import aq_inner

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ITeamPortlet(IPortletDataProvider):
    """A portlet showing information on teams
    """
    limit = schema.Int(
                title=_(u"Limit"),
                description=_(u"Specify the maximum number of items to show in the portlet. "
                                "Leave this blank to show all items."),
                default=None,
                required=False
                )

    sort_on = schema.Choice(
                title=_(u"Sort on criteria"),
                description=_(u"Choose the criteria on which to sort the items."),
                required=True,


                vocabulary=schema.vocabulary.SimpleVocabulary(
                        (schema.vocabulary.SimpleTerm(
                                                    'name',
                                                    title=_(u'Name'),
                                                    ),
                            schema.vocabulary.SimpleTerm(
                                                    'created',
                                                    title=_(u'Creation Date'),
                                                    ),
                            schema.vocabulary.SimpleTerm(
                                                    'modified',
                                                    title=_(u'Modification Date'),
                                                    ),
                        )
                    ),
                )


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(ITeamPortlet)

    limit = None
    show_dates = False
    sort_on = None

    def __init__(self, limit=None, sort_on=None, show_dates=False):
        self.limit = limit
        self.sort_on = sort_on

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Team Portlet"

class Renderer(base.Renderer):
    """Portlet renderer.
    """

    _template = ViewPageTemplateFile('teamportlet.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        nearest_folder = context
        while getattr(nearest_folder, 'portal_type', None) not in\
                ['team', 'Folder']:
            nearest_folder = nearest_folder.__parent__
        self.nearest_folder = "/".join(nearest_folder.getPhysicalPath())
        self.portal_state = getMultiAdapter(
                            (context, self.request),
                            name=u'plone_portal_state'
                            )
        self.anonymous = self.portal_state.anonymous()
        plone_tools = getMultiAdapter(
                            (context, self.request),
                            name=u'plone_tools'
                            )
        self.catalog = plone_tools.catalog()
        self.mtool = plone_tools.membership()

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return True

    @memoize
    def get_projects_for_current_member(self):
        limit = self.data.limit
        member = self.portal_state.member()
        member_id = member.getId()
        brains = []
        for index in  ['getProjectMembers', 'getProjectManagers']:
            query = {
                'portal_type':          'team',
                'sort_on':              'modified',
                'sort_order':           'reverse',
                'sort_limit':           limit,
                index:                  member_id,
            }
            brains += self.catalog(query)
        return brains

    def is_admin(self):
        member = self.portal_state.member()
        return member.has_role('Manager')

    def is_member_or_admin(self):
        if self.is_admin:
            return True
        # TODO: Check for membership in groups
        return member.getProperty('fullname') in self.context.members + self.context.managers

    def current_project(self):
        project = self.get_current_project()
        if project:
            return dict(project = project,
                        managers = self.project_managers(project),
                        members = self.project_members(project),
                        )
        else:
            return False
    
    def get_current_project(self):
        brains = []
        current_path = self.context.getPhysicalPath()
        
        while len(current_path)>1:
            path = '/'.join(current_path)
            query = {
                'portal_type': 'team',
                'path':        dict(query=path,depth=0),
                }
            brains = self.catalog(query)
            if len(brains) == 1:
                return brains[0]
            else:
                current_path = current_path[:-1]
        return False
    
    def project_members(self, project):
        """ returns useful data from members
        """
        members = project.getProjectMembers
        if members:
            for member_id in members:
                member = self.mtool.getMemberById(member_id) 
                if member:
                    yield dict(name = str(member.getProperty('fullname', '')),
                               email = str(member.getProperty('email', '')),)

    def project_managers(self, project):
        """ returns useful data from managers
        """
        managers = project.getProjectManagers
        if managers:
            for member_id in managers:
                member = self.mtool.getMemberById(member_id)
                if member:
                    yield dict(name = str(member.getProperty('fullname', '')),
                               email = str(member.getProperty('email', '')),)

class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(ITeamPortlet)
    label = _(u"Add Team Portlet")
    description = _(u"This portlet displays your projects.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(ITeamPortlet)
    label = _(u"Edit Team Portlet")
    description = _(u"This portlet displays your projects.")
