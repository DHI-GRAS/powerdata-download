from powerdata_download import query
import urllib
#import datetime


def download(start_date=None, end_date=None, parameters=[], identifier=None,
             extent=None, filename=None):

    url = query.build_query_url(start_date=start_date, end_date=end_date,
                                identifier=identifier, extent=extent,
                                parameters=parameters, output_list=["NETCDF"])
    data_link = query._get_link_from_url(url)
    urllib.request.urlretrieve(data_link, filename)

#download(start_date=datetime.date(2005,7,1),end_date=datetime.date(2005,7,31),parameters=["ALLSKY_SFC_SW_DWN"],identifier="Regional",extent={'xmin':-40,'xmax':-70,'ymin':-38,'ymax':-66},filename="/home/pako/repos/powerdata-download/powerdata_download/test1.nc")

