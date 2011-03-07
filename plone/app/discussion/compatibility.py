import pkg_resources
PLONE_41 = False
PLONE_40 = False
PLONE_33 = False
try:
    pkg_resources.get_distribution('Plone>=4.0.999999')
    PLONE_41 = True
except pkg_resources.VersionConflict:
    try:
        pkg_resources.get_distribution('Plone>=3.99999')
        PLONE_40 = True
    except pkg_resources.VersionConflict:
        PLONE_33 = True

PLONE_APP_VOCABULARIES_2_1_AND_UP = False
try:
    pkg_resources.get_distribution('plone.app.vocabularies>=2.1')
    PLONE_APP_VOCABULARIES_2_1_AND_UP = True
except pkg_resources.VersionConflict:
    pass
