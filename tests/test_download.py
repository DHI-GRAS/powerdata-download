import os
from powerdata_download import download


def test_download_query(tmpdir, download_kw):
    filenm = tmpdir.join("test.nc")
    download.download(**download_kw, filename=filenm)
    assert os.path.exists(filenm)
