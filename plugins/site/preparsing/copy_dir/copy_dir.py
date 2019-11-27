import shutil
from tqdm import tqdm
from sitefab.Plugins import SitePreparsing
from sitefab.SiteFab import SiteFab


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
        progress_bar = tqdm(total=len(targets), unit=' dir', desc="Copying directories", leave=False)
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
            progress_bar.update(1)
            log += "[OK]copied: '%s' to '%s'<br>" % (src, dst)

        if errors:
            return (SiteFab.ERROR, "CopyDir", log)
        else:
            return (SiteFab.OK, "CopyDir", log)