from urllib.request import urlretrieve
from urllib.parse import urlparse

import os


def download_entry(entry, download_dir, filetype='netcdf'):
    data_link = _get_link_from_entry(entry, filetype)
    o = urlparse(data_link)
    local_filename = os.path.join(download_dir, os.path.basename(o.path))
    urlretrieve(data_link, local_filename)
    return local_filename


def _get_link_from_entry(entry, filetype):
    try:
        return entry['outputs'][filetype]
    except KeyError:
        return []
