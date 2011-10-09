from zope import schema
from zope.component import getMultiAdapter #@UnresolvedImport
from zope.formlib import form
from zope.interface import implements

from Acquisition import aq_inner
from AccessControl import getSecurityManager
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.team.behaviors.team import ITeam
from collective.team import TeamMessageFactory as _

class ITeamPortlet(IPortletDataProvider):
    """A portlet showing information on teams
    """
    sort_on = schema.Choice(
                title=PMF(u"Sort on criteria"),
                description=PMF(u"Choose the criteria on which to sort the items."),
                required=True,
                default = 'sortable_title',
                vocabulary=schema.vocabulary.SimpleVocabulary(
                        (schema.vocabulary.SimpleTerm(
                                                    'sortable_title',
                                                    title=PMF(u'Title'),
                                                    ),
                            schema.vocabulary.SimpleTerm(
                                                    'created',
                                                    title=PMF(u'Creation Date'),
                                                    ),
                            schema.vocabulary.SimpleTerm(
                                                    'modified',
                                                    title=PMF(u'Modification Date'),
                                                    ),
                        ),
                    ),
                )


class Assignment(base.Assignment):
    """Portlet assignment.
    """
    implements(ITeamPortlet)
    
    sort_on = 'sortable_title'
    def __init__(self, sort_on='sortable_title'):
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
        has_teams = self.get_teams_for_current_member()
        in_team = self.current_team()
        return has_teams or in_team  

    @memoize
    def get_teams_for_current_member(self):
        sort_on = self.data.sort_on
        member = self.portal_state.member()
        member_id = member.getId()
        brains = []
        rids = []
        for index in  ['getTeamMembers', 'getTeamManagers']:
            query = {
                'portal_type':          'team',
                'sort_on':              sort_on,
                'sort_order':           'reverse',
                index:                  member_id,
                }
            for brain in self.catalog(query):
                rid = brain.getRID()
                if rid in rids:
                    continue
                rids.append(rid)
                brains.append(brain)
        return brains

    @memoize
    def current_team(self):
        for team in self.request.PARENTS:
            if ITeam.providedBy(team):
                sort_by_fullname = lambda x: x['username']
                admins = filter(lambda x:x, map(self.get_member_data, team.managers))
                admins.sort(key=sort_by_fullname)
                members = filter(lambda x:x, map(self.get_member_data, team.members))
                members.sort(key=sort_by_fullname)
                is_member = self.member_is_team_member(team)
                team =  {'title': team.title,
                        'description' : team.description,
                        'path' : team.absolute_url(),
                        'admins' : admins,
                        'members' : members,
                        'is_member' : is_member,
                        'results': []}
                return team
        return None
   
    def get_member_data(self, userid):
        acl_users = getToolByName(self.context, 'acl_users')
        member = acl_users.getUserById(userid)
        group = acl_users.getGroupById(userid)
        if member:
            username = member.getProperty("fullname") or member.getUserName()
            email = member.getProperty("email")
            membertype = 'user'
        if group:
            username = group.getGroupName()
            email = group.getProperty("email")
            membertype = 'group'
        if not group and not member:
            return member
        return dict(username=username, email=email, membertype=membertype)

    def member_is_team_member(self, team):
        if not self.mtool.isAnonymousUser():
            gtool = getToolByName(self.context, 'portal_groups')
            member = self.mtool.getAuthenticatedMember()
            member_id = member.getId()
            member_ids = [group.id for group in gtool.getGroupsByUserId(member_id)] 
            member_ids.append(member_id)
            if set(member_ids).intersection((team.members + team.managers)):
                return True
        return False


class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(ITeamPortlet)
    label = _(u"Add Team Portlet")
    description = _(u"This portlet displays your teams.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(ITeamPortlet)
    label = _(u"Edit Team Portlet")
    description = _(u"This portlet displays your teams.")
