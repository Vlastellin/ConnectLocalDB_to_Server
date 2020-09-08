activate_this = 'C:/Users/Администратор.WIN-OBTQMT3318V/Envs/SupervisionTool/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))
import os
import sys
import site
# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/Администратор.WIN-OBTQMT3318V/SupervisionTool/Lib/site-packages')
# Add the app's directory to the PYTHONPATH
sys.path.append('C:/tools/InServer')
sys.path.append('C:/tools/InServer/InServer')
os.environ['DJANGO_SETTINGS_MODULE'] = 'InServer.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
