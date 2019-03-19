from urllib.request import urlretrieve
from urllib.parse import urlparse

import os


def get_link_from_entry(entry, filetype):
    """Get download link from query result"""
    try:
        return entry['outputs'][filetype]
    except KeyError:
        raise RuntimeError(
            f'Unable to get download link for file type {filetype}. '
            f'Entry is {entry}.'
        )


def download_entry(entry, download_dir, filetype='netcdf'):
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
    urlretrieve(data_link, local_filename)
    return local_filename
