import shutil

from SiteFab.Plugins import SitePreparsing
from SiteFab.SiteFab import SiteFab


class CopyDir(SitePreparsing):
    """
    Copy directories
    """

    def process(self, unused, site, config):
        """ Process the content of the site once  
        :param FabSite site: the site object 
        """
        log = ""
        errors = False
        targets = config.targets
        
        for target in targets:
            try:
                src, dst = target.split('>')
                src = src.strip()
                dst = dst.strip()
            except:
                errors = True
                log += "[Failed] target '%s' is not properly formated<br/>" % target
                continue
            try:
                shutil.copytree(src, dst)
            except:
                errors = True
                log += "[Failed] failed to copy '%s' to '%s' <br/>" % (src, dst)
                continue

            log += "[OK]copied: '%s' to '%s'<br>" % (src, dst)
    
        if errors:
            return (SiteFab.ERROR, "CopyDir", log)
        else:
            return (SiteFab.OK, "CopyDir", log)