import logging
import traceback

from persistent import Persistent
from OFS.SimpleItem import SimpleItem
from smtplib import SMTPException

from zope.interface import implements, Interface, alsoProvides, Provides
from Products.ATContentTypes.interfaces import IATDocument
from plone.stringinterp.interfaces import IStringInterpolator
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.formlib import form

from zope import schema
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.MailHost.MailHost import MailHostError

from zope.component.interfaces import IObjectEvent
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.browser.formhelper import NullAddForm
from Acquisition import aq_inner

from Products.CMFPlone import PloneMessageFactory as PMF

logger = logging.getLogger("plone.contentrules")

class IMailNotifyAction(Interface):
    """Interface for the configurable aspects of the action.
    This is also used to create add and edit forms, below.
    """


class MailNotifyAction(SimpleItem):
    """The implementation of the action defined in IMailNotifyAction.
    """
    implements(IMailNotifyAction, IRuleElementData)

    element = "plone.actions.MailNotifyAction"
    summary = u"Benachrichtige Mitglieder"


class MailNotifyActionExecutor(object):
    """The executor for this action.
    This is registered as an adapter in configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, IMailNotifyAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        context = aq_inner(self.event.object)
        ploneutils = getToolByName(self.context, 'plone_utils')

        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, "You must have a Mailhost utility to \
execute this action"

        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        # interpolator = IStringInterpolator(obj)

        from_address = portal.getProperty('email_from_address')
        if not from_address:
            raise ValueError, "You must provide a source address for this \
action or enter an email in the portal properties"

        from_name = portal.getProperty('email_from_name').strip('"')
        source = '"%s" <%s>' % (from_name, from_address)

        recipients = self.recipients()

        # prepend interpolated message with \n to avoid interpretation
        # of first line as header
        message = "\n%s" % self.message()

        subject = self.subject()

        for email_recipient in recipients:
            try:
                # XXX: We're using "immediate=True" because otherwise we won't
                # be able to catch SMTPException as the smtp connection is made
                # as part of the transaction apparatus.
                # AlecM thinks this wouldn't be a problem if mail queuing was
                # always on -- but it isn't. (stevem)
                # so we test if queue is not on to set immediate
                mailhost.send(message, email_recipient, source,
                              subject=subject, charset=email_charset,
                              immediate=not mailhost.smtp_queue)
            except (MailHostError, SMTPException):
                logger.error(
                    """mailing error: Attempt to send mail in content rule failed.\n%s""" %
                    traceback.format_exc())

        return True

        
    def recipients(self):
        # get subscribers
        
        return ['bauer@starzel.de', ]


    def message(self):
        message = """Hallo Menschen!
Hier ist was passiert
        """
        return message

    def subject(self):
        subject = "Neue Inhalte im Intranet"
        
        return subject



class MailNotifyAddForm(NullAddForm):
    """An empty add form for portal type actions.
    """

    def create(self):
        return MailNotifyAction()



