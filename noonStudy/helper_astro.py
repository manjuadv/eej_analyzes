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

def moon_get_moon_phase_range_data_frame(start_date, end_date):
    from PyAstronomy import pyasl
    import numpy as np
    from datetime import datetime, timedelta
    import pandas as pd

    # Convert calendar date to JD
    # using the datetime package
    jd = start_date
    jd = pyasl.jdcnv(jd)
    no_of_days = (end_date - start_date).days
    jd = np.arange(jd, jd + no_of_days+1,1)
    mp = pyasl.moonphase(jd)

    dataSet = {'Day' : [], 'Phase' : [], 'Peak' : []}

    #previousHeighestValue = 0
    #previoutLowestValue = 1
    for d_offset, phase in enumerate(mp):
        day = (start_date + timedelta(days=d_offset)).replace(hour=12)
        dataSet['Day'] = np.append(dataSet['Day'], day)
        dataSet['Phase'] = np.append(dataSet['Phase'], phase)
        if d_offset > 0 and d_offset < (len(mp)-1):
            if mp[d_offset-1] <= phase > mp[d_offset+1]:
                dataSet['Peak'] = np.append(dataSet['Peak'], 'High')
            elif mp[d_offset-1] >= phase < mp[d_offset+1]:
                dataSet['Peak'] = np.append(dataSet['Peak'], 'Low')
            else:
                dataSet['Peak'] = np.append(dataSet['Peak'], None)
        else:
            dataSet['Peak'] = np.append(dataSet['Peak'], None)
    
    data_frame = pd.DataFrame(data=dataSet, index=dataSet['Day'], columns=['Phase','Peak'])
    return data_frame