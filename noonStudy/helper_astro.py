def moon_get_moon_phase(date):
    from PyAstronomy import pyasl
    import numpy as np

    # Convert calendar date to JD
    # using the datetime package
    jd = date
    jd = pyasl.jdcnv(jd)
    mp = pyasl.moonphase(jd)

    return mp[0]
        

def moon_get_moon_phase_range(start_date, end_date):
    from PyAstronomy import pyasl
    import numpy as np
    from datetime import datetime

    # Convert calendar date to JD
    # using the datetime package
    jd = start_date
    jd = pyasl.jdcnv(jd)
    no_of_days = (end_date - start_date).days
    jd = np.arange(jd, jd + no_of_days+1,1)
    mp = pyasl.moonphase(jd)

    return mp