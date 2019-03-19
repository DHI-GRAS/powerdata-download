import os
from powerdata_download import download, query


def test_download_query(tmpdir, download_kw):
    url = query.build_query_url(**download_kw)
    entry = query.get_entry(url)
    local_filename = download.download_entry(entry, download_dir=tmpdir)
    assert os.path.exists(local_filename)
