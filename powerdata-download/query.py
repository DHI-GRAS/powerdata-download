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


def build_query_url(start_date=None, end_date=None, parameters=[], identifier=None,
                    extent=None, output_list=None,user_community="SSE",temp_average="DAILY",
                    user="anonymous"):
    url = POWER_DATA_URL_BASE
    start_date, end_date = _date_logic(start_date, end_date)
    if start_date is not None and end_date is not None:
        datefmt = '%Y%m%d'
        url += '&startDate={}&endDate={}'.format(*[d.strftime(datefmt) for d in (start_date, end_date)])
    if len(parameters) <= _MAX_PARAMETERS:
        parameters_str = ",".join(parameters)
        url += '&parameters={}'.format(parameters_str)
    if identifier:
        url += '&identifier={}'.format(identifier)
    if extent and identifier == "SinglePoint":
        url += '&lat={lat}&lon={lon}'.format(**extent)
    if extent and identifier == "Regional":
        url += '&bbox={xmin},{xmax},{ymin},{ymax}'.format(**extent)
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

def _get_link_from_url(url):
    r = requests.get(url)
    catalogue = json.loads(r.text)
    try:
        return catalogue['outputs']['netcdf']
    except KeyError:
        return []
url = build_query_url(start_date=datetime.date(2005,7,1),end_date=datetime.date(2005,7,31),parameters=["ALLSKY_SFC_SW_DWN"],identifier="Regional",extent={'xmin':-40,'xmax':-70,'ymin':-38,'ymax':-66},output_list=["NETCDF"])
print(_get_link_from_url(url))
