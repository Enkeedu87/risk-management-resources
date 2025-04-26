# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 19:22:01 2025

@author: mograbgl
"""

import yfinance as yf

def download_and_fill_equity_data(Equity_ind, start_date, end_date, period_field, progress=True):
    """
    Download equity index data (and FX rates if needed), convert to USD if necessary,
    and fill the Equity_ind dictionary under the specified period_field.

    Parameters
    ----------
    Equity_ind : dict
        Dictionary containing equity indices and FX info.
    start_date : str
        Start date for data download (format: 'YYYY-MM-DD').
    end_date : str
        End date for data download (format: 'YYYY-MM-DD').
    period_field : str
        Field name to store the downloaded USD-adjusted DataFrame 
        (e.g., 'index_usd_values_pre_covid' or 'index_usd_values_with_covid').
    progress : bool, optional
        Show download progress bar (default is False).

    Returns
    -------
    dict
        Updated Equity_ind dictionary with downloaded data.
    """

    for tic in Equity_ind:
        fx_sym = Equity_ind[tic]["fx_symbol"]
        
        if fx_sym is None:
            # No FX conversion needed
            data = yf.download(
                tickers=[tic],
                start=start_date,
                end=end_date,
                progress=progress
            )["Close"]
            data.dropna(inplace=True)
            Equity_ind[tic][period_field] = data
        
        else:
            # Need FX conversion
            data = yf.download(
                tickers=[tic, fx_sym],
                start=start_date,
                end=end_date,
                progress=progress
            )["Close"]
            data.dropna(inplace=True)
            Equity_ind[tic][period_field] = (data[tic] / data[fx_sym]).to_frame(name=tic)

         

    return Equity_ind

