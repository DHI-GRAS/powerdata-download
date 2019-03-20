import os
import pytest
from powerdata_download import download, query


def test_download_query(tmpdir, download_kw):
    url = query.build_query_url(**download_kw)
    entry = query.get_entry(url)
    local_filename = download.download_entry(entry, download_dir=tmpdir)
    assert os.path.exists(local_filename)


def test_wrong_filetype(tmpdir, download_kw):
    url = query.build_query_url(**download_kw)
    entry = query.get_entry(url)
    with pytest.raises(RuntimeError):
        download.download_entry(entry, download_dir=tmpdir, filetype='ascii')


def test_wrong_query(tmpdir, download_kw):
    download_kw['parameters'] = []
    url = query.build_query_url(**download_kw)
    with pytest.raises(RuntimeError):
        query.get_entry(url)
