""" Utility functions and constants that will be used in the project.
"""

ADMIN_GROUP = 'Admin'
CLIENT_GROUP = 'Client'


def is_member(user, groups):
    """ Test if a user belongs to any of the groups provided.

    This function is meant to be used by the user_passes_test decorator to control access
    to views.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to a certain group.
    groups : list of str
        A list of the groups we are checking if the user belongs to.

    Returns
    ---------
    bool
        True if the user belongs to any of the groups. False otherwise
    """
    return any(map(lambda g: user.groups.filter(name=g).exists(), groups))


def is_admin(user):
    """ Test if a user has the admin group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to Admin.

    Returns
    ---------
    bool
        True if the user has Admin as a group
    """
    return is_member(user, [ADMIN_GROUP])


def is_client(user):
    """ Test if a user has the client group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to client.

    Returns
    ---------
    bool
        True if the user has client as a group.
    """
    return is_member(user, [CLIENT_GROUP])
