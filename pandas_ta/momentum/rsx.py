# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from pandas import DataFrame, Series, concat
from pandas_ta.utils import get_drift, get_offset, verify_series, signals
  
def rsx(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Relative Strength Xtra (inspired by Jurik RSX)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)
    
    # variables
    f0 = 0
    f8 = 0
    f10 = 0
    f18 = 0
    f20 = 0
    f28 = 0
    f30 = 0
    f38 = 0
    f40 = 0
    f48 = 0
    f50 = 0
    f58 = 0
    f60 = 0
    f68 = 0
    f70 = 0
    f78 = 0
    f80 = 0
    f88 = 0
    f90 = 0

    v4 = 0
    v8 = 0
    v10 = 0
    v14 = 0
    v18 = 0
    v20 = 0

    vC = 0
    v1C = 0
    
    # Calculate Result
    m = close.size
    result = [npNaN for _ in range(0, length - 1)] + [0]
    for i in range(length, m):
        if f90 == 0:
            f90 = 1.0
            f0 = 0.0
            if length - 1.0 >= 5:
                f88 = length - 1.0
            else:
                f88 = 5.0
            f8 = 100.0 * close[i]
            f18 = 3.0 / (length + 2.0)
            f20 = 1.0 - f18
        else:
            if f88 <= f90:
                f90 = f88 + 1
            else:
                f90 = f90 + 1
            f10 = f8
            f8 = 100 * close[i]
            v8 = f8 - f10
            f28 = f20 * f28 + f18 * v8
            f30 = f18 * f28 + f20 * f30
            vC = f28 * 1.5 - f30 * 0.5
            f38 = f20 * f38 + f18 * vC
            f40 = f18 * f38 + f20 * f40
            v10 = f38 * 1.5 - f40 * 0.5
            f48 = f20 * f48 + f18 * v10
            f50 = f18 * f48 + f20 * f50
            v14 = f48 * 1.5 - f50 * 0.5
            f58 = f20 * f58 + f18 * abs(v8)
            f60 = f18 * f58 + f20 * f60
            v18 = f58 * 1.5 - f60 * 0.5
            f68 = f20 * f68 + f18 * v18
            f70 = f18 * f68 + f20 * f70
            v1C = f68 * 1.5 - f70 * 0.5
            f78 = f20 * f78 + f18 * v1C
            f80 = f18 * f78 + f20 * f80
            v20 = f78 * 1.5 - f80 * 0.5
            if f88 >= f90 and f8 != f10:
                f0 = 1.0
            if f88 == f90 and f0 == 0.0:
                f90 = 0.0
        if f88 < f90 and v20 > 0.0000000001:
            v4 = (v14 / v20 + 1.0) * 50.0
            if v4 > 100.0:
                v4 = 100.0
            if v4 < 0.0:
                v4 = 0.0
        else:
            v4 = 50.0
        result.append(v4)
        # print('v4', v4)
    rsx = Series(result, index=close.index)

    # Offset
    if offset != 0:
        rsx = rsx.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        rsx.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        rsx.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    # print(rsx)
    # print(length)
    rsx.name = f"RSX_{length}"
    rsx.category = "momentum"

    signal_indicators = kwargs.pop("signal_indicators", False)
    if signal_indicators:
        signalsdf = concat(
            [
                DataFrame({rsx.name: rsx}),
                signals(
                    indicator=rsx,
                    xa=kwargs.pop("xa", 80),
                    xb=kwargs.pop("xb", 20),
                    xserie=kwargs.pop("xserie", None),
                    xserie_a=kwargs.pop("xserie_a", None),
                    xserie_b=kwargs.pop("xserie_b", None),
                    cross_values=kwargs.pop("cross_values", False),
                    cross_series=kwargs.pop("cross_series", True),
                    offset=offset,
                ),
            ],
            axis=1
        )

        return signalsdf
    else:
        return rsx


rsx.__doc__ = \
"""Relative Strength Xtra (rsx)

The Relative Strength Xtra is based on the popular RSI indicator and inspired by the work Jurik Research.
The code implemented is based on published code found at 'prorealcode.com'. This enhanced version of the rsi
reduces noise and provides a clearer, only slightly delayed insight on momentum and velocity of price movements.

Sources:
    http://www.jurikres.com/catalog1/ms_rsx.htm
    https://www.prorealcode.com/prorealtime-indicators/jurik-rsx/

Calculation:
    Refer to the sources above for information as well as code example.
  
Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14    
    drift (int): The difference period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""