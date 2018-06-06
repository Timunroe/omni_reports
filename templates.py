import utils_nums


def template_daily(d):
    s = f"{d['site']} report for {d['report date']}"
    s += '\n'
    s += '===================================================\n'
    s += 'SUMMARY: Page views, Unique visitors (UV), (V)isits\n'
    s += '===================================================\n'
    s += 'WEB       | Page      vs   |  KPI:  | Visits  KPI:\n'
    s += 'SITES     | Views     MA   |  PV/UV | vs MA   PV/V\n'
    s += '---------------------------+----------------------\n'
    for i, item in enumerate(d['summary']):
        s += f"{item['name'].ljust(10)} {(utils_nums.humanize_number(item['pv'])).rjust(7)}  {item['pv vs ma'].rjust(6)} |  "
        s += f"{str(item['pv / uv']).ljust(4, '0')}  |"
        s += f" {item['visits vs ma'].rjust(6)}  {str(item['pv / v']).ljust(4, '0')}\n"
        s += '---------------------------+-----------------------\n'
    s += 'MA = moving average = avg for past 90 days\n'
    s += f"R of M = Metroland minus {d['site']} stats\n"
    s += '=================================================='

    s += '\n\n'
    s += '=============================================\n'
    s += 'TRAFFIC     | % of | Page   | vs   \n'
    s += 'REFERRERS   | PV   | views  | MA  \n'
    s += '---------------------------------------------\n'
    for i, item in enumerate(d['referrers']):
        s += f"{i + 1}. {item['domain'].ljust(9)} {str(item['pv_ratio']).rjust(5)} "
        s += f"{ (utils_nums.humanize_number(str(item['pv']))).rjust(8)}  {item['diff_pv%'].rjust(7)}\n"
    s += "---------------------------------------------\n"
    s += "MA = moving average = avg for past 90 days\n"
    s += "============================================="

    s += '\n\n'
    s += '=============================================\n'
    s += 'DEVICE     | % of |  vs  | Page   |  vs   \n'
    s += 'TYPE       | PV   |  MA  | views  |  MA  \n'
    s += '---------------------------------------------\n'
    for i, item in enumerate(d['device types']):
        s += f"{i + 1}. {item['name'].ljust(8)} {str(item['%']).rjust(5)} "
        s += f"{str(item['diff_ratio']).rjust(6)} "
        s += f"{(utils_nums.humanize_number(str(item['pv']))).rjust(8)} {item['diff_pv%'].rjust(8)}\n"
    s += "---------------------------------------------\n"
    s += "MA = moving average = avg for past 90 days\n"
    s += "============================================="

    s += '\n\n'
    s += '=============================================\n'
    s += 'TOP        | Page  | %     |\n'
    s += 'STORIES    | Views | of PV | \n'
    for i, item in enumerate(d['top stories']):
        s += '---------------------------------------------\n'
        s += f"{i+1}. {str(item['asset']).ljust(8)}  {str(utils_nums.humanize_number(item['pv'])).rjust(6)}  {str(item['%']).rjust(4)}% "
        s += f" | By {item['article_info']['author']}, in {item['article_info']['section']}\n"
        s += f"  Hed: {item['article_info']['headline']}\n"
    s += '============================================='

    s += '\n\n'
    s += '=============================================\n'
    s += 'Top stories by % of traffic from FACEBOOK\n'
    s += '---------------------------------------------\n'
    for i, item in enumerate(d['facebook top stories']):
        s += f"{i + 1}. {item['%'].rjust(5)} | {item['headline']} | {utils_nums.humanize_number(str(item['pv']))} PV\n"
    s += "============================================="

    s += '\n\n'
    s += '=============================================\n'
    s += 'Top stories by % of traffic from TWITTER\n'
    s += '---------------------------------------------\n'
    for i, item in enumerate(d['twitter top stories']):
        s += f"{i + 1}. {item['%'].rjust(5)} | {item['headline']} | {str(item['pv'])} PV\n"
    s += "============================================="

    return s
