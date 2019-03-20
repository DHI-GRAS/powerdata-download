from urllib.request import urlretrieve
from urllib.parse import urlparse

import os
import shutil

MIN_FILE_SIZE_BYTES = 10e3


def get_link_from_entry(entry, filetype):
    """Get download link from query result"""
    try:
        return entry['outputs'][filetype]
    except KeyError:
        raise RuntimeError(
            f'Unable to get download link for file type {filetype}. '
            f'Entry is {entry}.'
        )


def download_entry(entry, download_dir, filetype='netcdf', skip_existing=False):
    """Download entry

    Parameters
    ----------
    entry : dict
        from query
    download_dir : str
        path to download directory
    filetype : str
        file type to download

    Returns
    -------
    str
        path to downloaded file
    """
    data_link = get_link_from_entry(entry, filetype)
    o = urlparse(data_link)
    local_filename = os.path.join(download_dir, os.path.basename(o.path))
    if os.path.isfile(local_filename) and skip_existing:
        pass
    else:
        _download_file_https(data_link, local_filename)
    return local_filename


def _download_file_https(url, target):
    temp_target = target + '.incomplete'
    urlretrieve(url, temp_target)

    filesize = os.path.getsize(temp_target)
    if filesize < MIN_FILE_SIZE_BYTES:
        raise RuntimeError(
            'Size of downloaded file is only {:.3f} B. Suspecting broken file({})'
            .format((filesize * 1e-3), temp_target))
    shutil.move(temp_target, target)
