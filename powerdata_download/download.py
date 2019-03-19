from powerdata_download import query
import urllib


def download(start_date=None, end_date=None, parameters=[], identifier=None,
             extent=None, filename=None):

    url = query.build_query_url(start_date=start_date, end_date=end_date,
                                identifier=identifier, extent=extent,
                                parameters=parameters, output_list=["NETCDF"])
    data_link = query._get_link_from_url(url)
    urllib.request.urlretrieve(data_link, filename)
