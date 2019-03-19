import pytest

import datetime


@pytest.fixture
def download_kw():
    return dict(
        start_date=datetime.date(2005, 7, 1),
        end_date=datetime.date(2005, 7, 31),
        parameters=["ALLSKY_SFC_SW_DWN"],
        identifier="Regional",
        extent=dict(xmin=-40,
                    xmax=-38,
                    ymin=-70,
                    ymax=-66
                    ),
        output_list=['NETCDF']
    )
