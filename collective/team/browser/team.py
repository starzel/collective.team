from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from five import grok
from json import dumps
from DateTime.DateTime import DateTime
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.site.hooks import getSite

from collective.team.behaviors.team import ITeam

class JSONView(grok.View):
    grok.context(ITeam)
    grok.require('zope2.View')

    def __call__(self):
        if not hasattr(self, 'site'):
            self.site = getSite()
        results = self.site.portal_catalog(
            path="/".join(self.context.getPhysicalPath()),
            portal_type=("Folder", "team"),
            sort_on="path")
        ordered = {}
        retval = []
        for result in results:
            path = result.getPath()
            parent_path = '/'.join(path.split('/')[:-1])
            title = result.Title
            new_elem = dict(title=title,
                             isFolder=True,
                             href=result.getURL(),
                             children=[],
                             key=path)
            if parent_path in ordered:
                ordered[parent_path]['children'].append(new_elem)
            else:
                retval.append(new_elem)
            ordered[path] = new_elem
        return dumps(retval)

    def strip_parents(self, results):
        for result in results:
            if result['children']:
                self.strip_parents(result['children'])
            result.pop('parent')

    def render(self, *args, **kwargs):
        pass

class View(grok.View):
    grok.context(ITeam)
    grok.require('zope2.View')

    def __call__(self, site = None):
        if site is None:
            site = getSite()
        self.site = site
        return super(View, self).__call__()

    def latest_docs(self):
        localize = self.site.translation_service.ulocalized_time
        all_portal_types = self.site.portal_catalog\
            .uniqueValuesFor('portal_type')
        all_portal_types = filter(lambda x: x not in ('Folder', 'team', 'Topic', 'Collection', 'Event'),
                                  all_portal_types)
        newest_docs = self.site.portal_catalog(
            path="/".join(self.context.getPhysicalPath()),
            sort_on='modified',
            portal_type=all_portal_types,
            sort_limit=5,
            sort_order='descending')[:5]
        return newest_docs

    def next_events(self):
        subject = ''
        if self.context.subject:
            subject = self.context.subject[0]
        next_events = self.site.portal_catalog(
            Subject = subject,
            sort_on='start',
            portal_type='Event',
            end={'query': DateTime(),
                 'range': 'min'},
            sort_limit=3,)[:3]
        return next_events

    def project_members(self):
            sort_by_fullname = lambda x: x['username']
            admins = filter(lambda x:x, map(self.get_member_data, self.context.managers))
            admins.sort(key=sort_by_fullname)
            members = filter(lambda x:x, map(self.get_member_data, self.context.members))
            members.sort(key=sort_by_fullname)
            project_members =  {'admins' : admins,
                                'members' : members,}
            return project_members

    def get_member_data(self, userid):
        member = self.site.acl_users.getUserById(userid)
        group = self.site.acl_users.getGroupById(userid)
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

    def help(self):
        help_docs = self.site.portal_catalog(
            path='/dipf/wissen/intranet/special-interest-groups/hilfe',
            portal_type=('Document', 'File', 'News Item'),
            sort_limit=10,)[:10]
        return help_docs
        


class AddFolder(grok.View):
    grok.context(ITeam)
    grok.require('zope2.View')

    def __call__(self):
        if not hasattr(self, 'normalizer'):
            self.normalizer = getUtility(IIDNormalizer)
        path = self.request.form['path']
        title = self.request.form['title']
        id = self.normalizer.normalize(title)
        folder = self.context.restrictedTraverse(path)
        folder.invokeFactory(id=id, type_name="Folder")
        new_ob = folder[id]
        new_ob.title = title
        new_ob.reindexObject()
        return ''

    def render(self):
        pass
