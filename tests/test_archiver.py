""""""
import pathlib
import tarfile

import pytest 

import archiver.archiver as archiver


#==================================================================================================
@pytest.mark.parametrize(
    ("include", "exclude", "outputs"),
    [
        (["*.toml",], None, ["pyproject.toml"]),
        (["*.py", "*.toml"], None, ["pyproject.toml", "python.py"]),
        (["**/*.py",], None, ["python.py", "subdirectory1/python1.py", "subdirectory1/python2.py", "subdirectory2/python1.py"]),
        (["*.log",], ["junk.*"], ["important.log"]),

    ]
)
def test_find_archive_fojbs(archive_dir, include, exclude, outputs):
    """"""
    fobjs = archiver.find_archive_fobjs(archive_dir, include=include, exclude=exclude)    
    fobjs = [str(fobj.relative_to(archive_dir)) for fobj in fobjs]
    assert sorted(fobjs) == sorted(outputs)


#==================================================================================================
@pytest.mark.parametrize(
    ("inputs", "outputs"),
    [
        (["pyproject.toml",], ["pyproject.toml",]),
        (["pyproject.toml", "python.py"], ["pyproject.toml", "python.py"]),
        (["subdirectory1/python1.py",], ["subdirectory1/python1.py",]),
    ]
)
def test_archive_fobjs(tmp_path, archive_dir, inputs, outputs):
    """"""
    fobjs = [archive_dir / fname for fname in inputs]
    aname = archiver.archive_fobjs(fobjs, aname=tmp_path / "archive.tar", root=archive_dir)
    
    assert aname.exists()
    with tarfile.open(aname, "r") as fobj:
        assert sorted(fobj.getnames()) == sorted(outputs)


def test_archive_fobjs_flatten(tmp_path, archive_dir):
    """"""
    fobjs = [archive_dir / "subdirectory1/python1.py",]
    aname = archiver.archive_fobjs(fobjs, aname=tmp_path / "archive.tar", flatten=True, root=archive_dir)
    
    assert aname.exists()
    with tarfile.open(aname, "r") as fobj:
        assert fobj.getnames() == ["python1.py",]
   

def test_archive_fobjs_exists(tmp_path, archive_dir):
    """"""
    aname = tmp_path / "archive.tar"
    aname.touch()
    fobjs = [archive_dir / "python.py"]

    with pytest.raises(OSError, match=r'Archive path ".+" exists'):
        archiver.archive_fobjs(fobjs, aname=aname, exist_ok=False)


#==================================================================================================
def test_compress_fobj(tmp_path, archive_dir):
    """"""
    tmp = tmp_path / "tmp"
    tmp.touch()
    fname = archiver.compress_fobj(tmp)
    assert fname.is_file()


def test_compress_fobjs(tmp_path, archive_dir):
    """"""
    tmp1 = tmp_path / "tmp1"
    tmp2 = tmp_path / "tmp2"
    tmp1.touch()
    tmp2.touch()
    fnames = archiver.compress_fobjs([tmp1, tmp2])
    assert len(fnames) == 2
    assert fnames[0].is_file()
    assert fnames[1].is_file()