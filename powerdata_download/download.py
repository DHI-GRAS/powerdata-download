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


def download_entry(
        entry, download_dir=None, local_filename=None, filetype='netcdf', skip_existing=False
):
    """Download entry

    Parameters
    ----------
    entry : dict
        from query
    download_dir : str, optional
        path to download directory
        ignored if local_filename is specified
    local_filename : str, optional
        complete path to local file name
        overrides download_dir / <original-name>
    filetype : str
        file type to download

    Returns
    -------
    str
        path to downloaded file
    """
    if download_dir is None and local_filename is None:
        raise ValueError('Specify either download_dir or local_filename.')
    data_link = get_link_from_entry(entry, filetype)
    o = urlparse(data_link)
    if local_filename is None:
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
