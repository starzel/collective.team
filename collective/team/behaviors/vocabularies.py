from five import grok

from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

from collective.team import TeamMessageFactory as _

class TeamWorkflowPolicies:
    grok.implements(IVocabularyFactory)
    def __call__(self, context):
        context = getattr(context, 'context', context)
        placeful_workflow = getToolByName(context, 'portal_placeful_workflow', None)
        items = []
        if placeful_workflow is not None:
            if PLACEFUL_WORKFLOW_POLICY in placeful_workflow.objectIds():
                items.append((_(u"Default project workflow"), 'collective_team_placeful_workflow'))
        items.sort()
        return SimpleVocabulary.fromItems(items)

class TeamGloballyAllowedTypes:
    grok.implements(IVocabularyFactory)
    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal_types = getToolByName(context, 'portal_types')
        items = []
        for fti in portal_types.listTypeInfo():
            if getattr(fti, 'globalAllow', lambda: False)() == True and fti.title:
                items.append((fti.title, fti.getId(),))
        return SimpleVocabulary.fromItems(items)

grok.global_utility(TeamWorkflowPolicies, provides=IVocabularyFactory, name="collective.team.WorkflowPolicies", direct=False)
grok.global_utility(TeamGloballyAllowedTypes, provides=IVocabularyFactory, name="collective.team.AddableTypes", direct=False)
