import datetime
import requests
import json

POWER_DATA_URL_BASE = 'https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?request=execute'
_TZERO = datetime.time()
_MAX_PARAMETERS = 20


def _date_logic(start_date, end_date):

    if start_date is None and end_date is None:
        return None, None
    elif end_date is None:
        end_date = start_date + datetime.timedelta(days=1)
    elif start_date is None:
        start_date = end_date - datetime.timedelta(days=1)
    return start_date, end_date


def build_query_url(start_date=None, end_date=None, parameters=None, identifier=None,
                    extent=None, output_list=None, user_community="SSE", temp_average="DAILY",
                    user="anonymous"):
    """Build POWER query URL

    Parameters
    ----------
    start_date, end_date : datetime.datetime, optional
        date range
    parameters : list of str
        parameters to download
    identifier : str in [SinglePoint, Regional, Global], optional
        region identifier
    extent : dict, optional
        with keys xmin, xmax, ymin, ymax if identifier is Regional
        with keys lat, lon if identifier is SinglePoint
    output_list : list of str
        list of output file formats
    **other
        see API docs

    Returns
    -------
    str
        query URL
    """
    url = POWER_DATA_URL_BASE
    start_date, end_date = _date_logic(start_date, end_date)
    if start_date is not None and end_date is not None:
        datefmt = '%Y%m%d'
        url += '&startDate={}&endDate={}'.format(*[d.strftime(datefmt)
                                                   for d in (start_date, end_date)])
    if parameters and len(parameters) <= _MAX_PARAMETERS:
        parameters_str = ",".join(parameters)
        url += '&parameters={}'.format(parameters_str)
    if identifier:
        url += '&identifier={}'.format(identifier)
    if extent and identifier == "SinglePoint":
        url += '&lat={lat}&lon={lon}'.format(**extent)
    if extent and identifier == "Regional":
        # lower-left latitude,lower-left longitude,upper-right latitude,upper-right longitude
        # (decimal degrees and no spaces between commas)
        url += '&bbox={ymin},{xmin},{ymax},{xmax}'.format(**extent)
    if output_list:
        output_str = ",".join(output_list)
        url += '&outputList={}'.format(output_str)
    if user:
        url += '&user={}'.format(user)
    if user_community:
        url += '&userCommunity={}'.format(user_community)
    if temp_average:
        url += '&tempAverage={}'.format(temp_average)
    return url


def get_entry(url):
    """Call query URL and check returned entry

    Parameters
    ----------
    url : str
        POWER query URL

    Returns
    -------
    dict
        entry returned by query

    Raises
    ------
    RuntimeError
        when API returned error
    """
    r = requests.get(url)
    r.raise_for_status()
    entry = json.loads(r.text)
    for message in entry.get('messages', []):
        if 'Alert' in message:
            raise RuntimeError(message)
    return entry
