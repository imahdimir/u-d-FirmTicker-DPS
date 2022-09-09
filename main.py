"""

    """

import asyncio
from io import StringIO

import pandas as pd
from githubdata import GithubData
from mirutil.async_requests import get_reps_texts_async
from mirutil.df_utils import save_df_as_a_nice_xl as sxl
from mirutil.utils import print_list_as_dict_fmt
from mirutil.utils import ret_clusters_indices


class GDUrl :
    ftic = 'https://github.com/imahdimir/d-FirmTickers'
    cur = 'https://github.com/imahdimir/u-d-FirmTicker-DPS'
    trg0 = 'https://github.com/imahdimir/d-0-FirmTicker-DPS'
    trg = 'https://github.com/imahdimir/d-FirmTicker-DPS'

gu = GDUrl()

class Constant :
    burl = 'http://tsetmc.com/tsev2/data/DPSData.aspx?s='

cte = Constant()

class ColName :
    ftic = 'FirmTicker'
    url = 'url'
    res = 'res'
    pub = 'PublicationJDate'
    maj = 'تاریخ مجمع'
    fisy = 'FiscalYearJDate'
    afpr = 'سود یا زیان پس از کسر مالیات'
    pr = 'سود قابل تخصیص'
    stpr = 'سود انباشته پایان دوره'
    dps = 'DPS'

c = ColName()

fu0 = get_reps_texts_async

def conv_2_df_each_row(res) :
    if res is None :
        return pd.DataFrame()

    res = res.replace(';' , '\n')
    fi = StringIO(res)
    df = pd.read_csv(fi , sep = '@' , header = None)
    df.columns = [c.pub , c.maj , c.fisy , c.afpr , c.pr , c.stpr , c.dps]
    return df

def main() :
    pass

    ##
    gd_ftic = GithubData(gu.ftic)
    gd_ftic.overwriting_clone()
    ##
    df = gd_ftic.read_data()
    ##
    df[c.url] = cte.burl + df[c.ftic]
    ##
    df[c.res] = None
    df1 = df.copy()
    ##
    while not df1.empty :
        msk = df[c.res].isna()
        df1 = df1[msk]

        clus = ret_clusters_indices(df1)

        for se in clus :
            si , ei = se
            print(se)

            inds = df1.iloc[si :ei].index

            urls = df.loc[inds , c.url]

            ress = asyncio.run(fu0(urls))

            df.loc[inds , c.res] = ress

            # break

        # break

    ##
    msk = df[c.res].eq('')
    df.loc[msk , c.res] = None

    ##
    dfa = pd.DataFrame()

    for ind , ro in df.iterrows() :
        res = ro[c.res]
        df1 = conv_2_df_each_row(res)
        df1[c.ftic] = ro[c.ftic]
        dfa = pd.concat([dfa , df1] , axis = 0)

    ##
    dfa = dfa.drop_duplicates()

    ##
    print_list_as_dict_fmt(dfa.columns)
    cols = {
            "FirmTicker"                   : None ,
            "PublicationJDate"             : None ,
            "تاریخ مجمع"                   : None ,
            "FiscalYearJDate"              : None ,
            "سود یا زیان پس از کسر مالیات" : None ,
            "سود قابل تخصیص"               : None ,
            "سود انباشته پایان دوره"       : None ,
            "DPS"                          : None ,
            }
    ##
    dfa = dfa[cols.keys()]

    ##
    cols = [c.pub , c.maj , c.fisy]
    for col in cols :
        dfa[col] = dfa[col].str.replace('/' , '-')

    ##

    gd_trg0 = GithubData(gu.trg0)
    gd_trg0.overwriting_clone()

    ##
    dft0 = gd_trg0.read_data()
    ##
    dft0 = pd.concat([dft0 , dfa] , axis = 0)
    ##
    dft0 = dft0.drop_duplicates()
    ##
    fp = gd_trg0.data_fp
    sxl(dft0 , fp)
    ##
    msg = 'data updated by: '
    msg += gu.cur
    ##

    gd_trg0.commit_and_push(msg)

    ##
    c2k = {
            c.ftic : c.ftic ,
            c.pub  : c.pub ,
            c.maj  : c.maj ,
            c.fisy : c.fisy ,
            c.dps  : c.dps ,
            }

    dft0 = dft0[c2k.keys()]

    ##

    gd_trg = GithubData(gu.trg)
    gd_trg.overwriting_clone()

    ##
    dft = gd_trg.read_data()
    ##
    dft = pd.concat([dft , dft0] , axis = 0)
    ##
    dft = dft.drop_duplicates()

    ##


    ##
    fp = gd_trg.data_fp
    sxl(dft , fp)
    ##

    msg = 'data updated by: '
    msg += gu.cur
    ##

    gd_trg.commit_and_push(msg)

    ##


    gd_trg0.rmdir()
    gd_trg.rmdir()
    gd_ftic.rmdir()


    ##

##
if __name__ == "__main__" :
    main()

##
# noinspection PyUnreachableCode
if False :
    pass

    ##


    ##


    ##

##
