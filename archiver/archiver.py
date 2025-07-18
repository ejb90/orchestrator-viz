""""""
import argparse
import datetime
import grp
import gzip
import os
import pathlib
import pwd
import re
import shutil
import tarfile


# class Settings(settings.Settings):
class Settings:
    """"""
    def __init__(self):
        """"""
        self.include = [
            "**/*.csv",
            "**/*.df",
            "**/*.err",
            "**/*.in",
            "**/*.json",
            "**/*.log",
            "**/*.out",
            "**/*.png",
            "**/*.toml",
            "**/*.yaml",

        ]
        self.exclude = []
        self.search_root = pathlib.Path()

        self.archive = False
        self.compress = False
        self.copy = False
        self.move = False
        self.owner = None
        self.group = None
        self.perms_file = None
        self.perms_dir = None

        self.archive_root = pathlib.Path()
        self.archive_path = None
        self.path_pattern = []
        self._patterns = {}
        self.user_patterns = {}
    
    def get_path_pattern(self):
        """"""
        datetime_obj = datetime.datetime.now()

        self._patterns = {
            "user": os.environ.get("USER"),
            "year": datetime_obj.year,
            "month": datetime_obj.year,
            "day": datetime_obj.day,
            "date": datetime_obj.date(),
            "date_time": datetime_obj.isoformat(),
            "model": None,
            "step": None,
        }
        self._patterns.update(self.user_patterns)

    def build_storage_path(self):
        """""" 
        self.get_path_pattern()

        self.archive_path = self.archive_root
        for part in self.path_pattern:
            self.archive_path = self.archive_path / str(self._patterns.get(part, ""))


def find_storage_fobjs(root, include, exclude=None):
    """"""
    matches = [path for pattern in include for path in root.glob(pattern)]
    exclusions = [path for pattern in exclude for path in root.glob(pattern)] if exclude else []
    matches = set([path for path in matches if path not in exclusions])
    return matches


def archive_fobjs(fobjs, aname=pathlib.Path("archive.tar"), exist_ok=False, flatten=False, root=pathlib.Path()):
    """"""
    if not exist_ok and aname.exists():
        raise OSError(f'Archive path "{aname}" exists')
    
    with tarfile.open(aname, "w") as tar:
        for item in fobjs:
            if flatten:
                arcname = item.name
            else:
                try:
                    arcname = item.relative_to(root)
                except ValueError:
                    arcname = item
            tar.add(item, arcname=arcname)
    
    return aname


def compress_fobjs(fobjs):
    """"""
    return [compress_fobj(fobj) for fobj in fobjs]
        

def compress_fobj(fobj):
    """
    """
    fname = fobj.with_suffix(fobj.suffix + '.gz')

    with open(fobj, 'rb') as fin, gzip.open(fname, 'wb') as fout:
        shutil.copyfileobj(fin, fout)
    return fname


def change_perms(fobjs, perm):
    """"""
    for fobj in fobjs:
        fobj.chmod(perm)


def change_group(fobj, group):
    """"""
    try:
        gid = grp.getgrnam(group).gr_gid
    except KeyError:
        raise Exception(f'Requested group "{group}" is not known')

    os.chown(fobj, -1, gid)


def change_owner(fobj, owner):
    """"""
    try:
        uid = pwd.getpwnam(owner).uid
    except KeyError:
        raise Exception(f'Requested group "{owner}" is not known')

    os.chown(fobj, uid, -1)


def parse_args():
    """"""
    parser = argparse.ArgumentParser(description="Archiver CLI inputs")

    parser.add_argument("--cfg", type=pathlib.Path, default=pathlib.Path("archive.yaml"), help="Configuration file path")
    
    return parser.parse_args()


def main():
    """"""
    cfg = Settings()
    storage_objs = find_storage_fobjs(cfg.search_root)

    if cfg.archive:
        storage_objs = archive_fobjs(storage_objs, aname=cfg.search_root / pathlib.Path("archive.tar"), exist_ok=cfg.exist_ok, flatten=cfg.flatten, root=cfg.search_root)
        storage_objs = [storage_objs,]
    
    if cfg.compress:
        storage_objs = compress_fobjs(storage_objs)
        # Todo - if archive == True, there is a temporary .tar file which needs to be removed here when the tar.gz is made
    
    if cfg.owner: 
        for fobj in storage_objs:
            change_owner(fobj)
    if cfg.group:
        for fobj in storage_objs:
            change_group(fobj)
    if cfg.perms_file:
        for fobj in storage_objs:
            if fobj.is_file():
                change_perms(fobj, cfg.perms_file)
    if cfg.perms_dir:
        for fobj in storage_objs:
            if fobj.is_dir():
                change_perms(fobj, cfg.perms_dir)
    
    if cfg.copy:
        for fobj in storage_objs:
            shutil.copy2(fobj, cfg.archive_path / fobj.name)
    if cfg.move:
        for fobj in storage_objs:
            fobj.rename(cfg.archive_path / fobj.name)
