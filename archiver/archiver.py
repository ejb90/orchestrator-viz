""""""
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


def find_archive_fobjs(root, include, exclude=None):
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


def move_fobjs(fobjs, dest):
    """"""
    shutil.copy2(fobjs, dest)


def build_archive_dir(root, pattern):
    """"""
    path = root
    for part in pattern:
        path = path / part
    return path
