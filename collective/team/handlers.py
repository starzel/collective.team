from Acquisition import aq_base
from zope.interface import implements
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from collective.team.behaviors.team import ITeam

def _get_role_permission_for_fti(context, fti):
    """Helper method to get hold of a RolePermission for a given FTI.
    """
    factory = getattr(fti, 'factory', None)
    product = getattr(fti, 'product', None)
    dispatcher = getattr(context, 'manage_addProduct', None)

    if factory is None or product is None or dispatcher is None:
        return None

    try:
        product_instance = dispatcher[product]
    except AttributeError:
        return None

    factory_method = getattr(product_instance, factory, None)
    if factory_method is None:
        return None

    factory_instance = getattr(factory_method, 'im_self', None)
    if factory_instance is None:
        return None

    factory_class = factory_instance.__class__
    role_permission = getattr(factory_class, factory+'__roles__', None)
    if role_permission is None:
        return None

    return role_permission

def get_factory_permission(context, fti):
    """Return the factory perimssion of the given type information object.
    """
    role_permission = _get_role_permission_for_fti(context, fti)
    if role_permission is None:
        return None
    return role_permission.__name__

def updateIndexedSecurity(team, event):
    """
    Some properties are used for local roles. The catalog can find items
    independent of the current context, it is therefor impossible to tell
    which local roles a user has for a given result.
    Plone has an index that helps to define who can see things. Because
    we cannot know the local roles for a given user or group for search
    results, the catalog also indexes the users and groups that have
    Access because of local roles.
    That has implications: If we modify the local roles, the subobject
    must be reindexed, at least the indexes that store security information.
    Thats what this event handler does.
    """
    team.reindexObjectSecurity(skip_self = True)

def enable_addable_types(team, event):
    """Give the given role the add permission on all the selected types.
    """
    portal_types = getToolByName(team, 'portal_types')
    relevant_roles = ['Editor', 'Reviewer']

    for fti in portal_types.listTypeInfo():
        type_id = fti.getId()

        permission = get_factory_permission(team, fti)
        if permission is not None:
            roles = [r['name'] for r in team.rolesOfPermission(permission) if r['selected']]
            acquire = bool(team.permission_settings(permission)[0]['acquire'])
            for role in relevant_roles:
                if role not in roles:
                    roles.append(role)
            team.manage_permission(permission, roles, acquire)

