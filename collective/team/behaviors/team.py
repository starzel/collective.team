# encoding=utf-8
from plone.directives import form
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from rwproperty import getproperty, setproperty
from zope import schema
from zope.component import adapts
from zope.interface import implements, alsoProvides, Interface
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.site.hooks import getSite
from collective.team import TeamMessageFactory as _

class ITeam(form.Schema):
    
    form.widget(members=AutocompleteMultiFieldWidget)
    members = schema.List(
        title=_(u"Members"),
        required=False,
        value_type=schema.Choice(
            vocabulary=u"plone.principalsource.Principals")
        )
    
    form.widget(managers=AutocompleteMultiFieldWidget)
    managers = schema.List(
        title=_(u"Managers"),
        required=False,
        value_type=schema.Choice(
            vocabulary=u"plone.principalsource.Principals")
        )
        
alsoProvides(ITeam, form.IFormFieldProvider)
