#####
# configuration for the mdsrv wsgi app

# leave empty if no virtualenv is needed
APP_ENV = ''

# leave empty to use default config
APP_CFG = ''


#####
# do not change anything below unless you are sure
# see http://flask.pocoo.org/docs/deploying/mod_wsgi/


import os, sys

if APP_ENV:
    if sys.version_info[0] > (3,):
        activate_this = os.path.join( APP_ENV, 'activate_this.py' )
        with open( activate_this ) as f:
            code = compile( f.read(), activate_this, 'exec' )
            exec( code, dict( __file__=activate_this ) )
    else:
        activate_this = os.path.join( APP_ENV, 'activate_this.py' )
        execfile( activate_this, dict( __file__=activate_this ) )

from mdsrv import app as application
if APP_CFG:
    application.config.from_pyfile( APP_CFG )

