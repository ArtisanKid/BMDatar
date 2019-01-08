#!/usr/local/bin/python3

import os
import sys
import traceback
import pymysql
import time
import Imager
import Emailer

invalid_accounts = ['PBNAD5RVRVJXY7HYBBILBSG5AGASTBHK',
'RFP43RJZZXHDBL8IXNJXNSONW8V6FUJE',
'QT6IR1BRZZHK8SNNEOER5TTS68HKQGFI',
'6OSQMWQABQIVHCY0XMMSQU2HMBIPZ1NX',
'ZDWH7RE0AGVXKTDIJDGVOKUVFACUS18D',
'MZGTUBOCMHJSRMSYKX87PS9IVHXPZ8UW',
'8TDZRHSQCJ0CKJW9OCQDJNEMNSZGEVYD',
'MLRBNTQF14QMUP2QALRVIJYWTNBBV50X',
'9IFTDCHZLNYNREZQD79YJPRTQG8FFXTO',
'VG7b110EWKNbImyWSCG4VIG5zB90RSdx',
'SV3fZ9M7Mn8psfheZNhVo4T3BFl3fpPV',
'zWOraRCC83Zrt9ZPiy3v1n6D5tt2mOWX',
'2AbrSLBYsmgyBtiTOruBtxYk0HVxXoxR',
'Cj0uMmOtgZLQorYsSKzOdaqB9UUzWbcB',
'y3bZeYMk7om6ARhllGAevSQT5QWTfWHQ',
'OHTA4AENTVJHS1FCGRN02CCBCK5VWAG7',
'9CF5QE2JPTTNBPINOOUC0G8SLRRLKQNY',
'nSwqO0RAoYcq8oUUzLEEdqAytbVtHDHB',
'SHQAIX6XBEC5QTNBIL3ZUBDIEWRHB5VX',
'VHBCFVXO06NZFLBYQPEKUX7UKFZXLY02',
'8S2w4FRcfQeJYs6UB3FAU9oqKGTVigiO',
'ryaJQKxcGMGvQQcKQmCtIEj4BFpR79Pu',
'P46YH2KBPYZUBXGJVDKEIV9RNUZ75BNH',
'ELOH7P60PBDWIRMYZA60HXNFGM5AQMOL',
'EIONJ0KQSOJKTD5AL73TAUX0NURRBBTO',
'TMXXHPJPOD7XIKDXJVQKI0TZFHPCF1N2',
'ooMF50V5NKnapfpk0Sa2dFPRLPb1pK4x',
'QW7CZQ0MFGTQCDZPKDBLGF3DPED7LTZB',
'yUa27aqJCyrZaDYwLNIC02u4FYWtmW1f',
'P0GoOBkYqYkujC1dzHhynCb5sBDu88yC',
'N1PRBRU6LVKALSNDGADPEAASMFD8QF5L',
'WFAX1Z892R35XXCZQPGXBOHGPUIDWY4E',
'H2IVDSF1UXJTXV8ZG7EXEPDMY6N8GILP',
'Z5S7CVXV07FOIQDYBHM4PVV1TS7PLR00',
'D171L2WFRYC0ZOSEUL1AB4FC28QCUE3F',
'bitmax-test-0',
'bitmax-test-1',
'bitmax-test-2',
'bitmax-test-3',
'bitmax-test-4',
'bitmax-test-5',
'bitmax-test-6',
'bitmax-test-7',
'bitmax-test-8',
'bitmax-test-9',
'HSF2XLVA0WWQPAAKMOFQIKFXJ1RJ9L7T',
'AUM92NRE8WW1ZJPYXLIAIKMOAQIEAITD',
'5JAN9SID9OF9SRQGRXXW7VBVITBPPO6W',
'4qxGu7I8HOwPLdvNLkRvWEJD8EwMg329',
'IBSMYAWJMBF6GD47IGSZTGMA69UVXNFP',
'MPXFNEYEJIJ93CREXT3LTCIDIJPCFNIX',
'G7HUJ1H5E6CSWXWZGJRQUSXXGGCDNJ7A',
'KU0VKULJ95QGILC6RPEFPMBNLB7EYYUW',
'PERJX3M2D5CTH3WTRAGRZR5GWY1P64XX',
'TLG5GILYA55PGIJKH0YMNFO1GSQB9YX3',
'Z2RNADEAFM09K95P5HQNFP4GED6D7OMT',
'4RAZUCQ0BCLWWJQJNBJIIRKBGTB3K3V3',
'9SCP3ZHJYIVQ4WTZJI67YPI6RUC7SL44',
'W9TIEVMEI8NJNNPJX9QJZWS3CIFX6ESM',
'E1SSRUQTAAKTYFFSY2A9GAYUUE2ZZYNZ',
'XY0YQQHWYRMSCZEY31COQE27QBIXP7ZQ',
'LVPZVBAAZOUTLN6I5IXAWLYQZXRBPPVO',
'YTB9IKPD4CV2YLHVZJ4HECRWVS9KUNJY',
'YTMFKIKRHEYIKBB4FAVB8U67QNWAWGVC',
'XOT1XEK7PJZU3XFOJEN11NSD9YLGHLHS',
'034BEVSM4IGYYGKGODY2KRVPX4SQOSYO',
'RV9SZQKLE0HN1HSTETMMEJFWH0I9LWPO',
'perm-lock',
'41D5CEIQASZF8CQ36KPKQSCJ6CJXYDFB',
'pool2-bitmax',
'ZAC74DAX1W4JNEEEUW933JQKOUJZRPK6',
'EHGJNRJMQQNPTHUPEWYSA4TQBL6OMCUW',
'OIU90DCKZ7GX03RSLZXKS1I8OBJ9YDD9',
'AADJB0OSCZVTHHBWPCLMWMKCSPGFIP9Y',
'term-deposit-fund',
'vault-bitmax.io-account',
'IRACSDE1YEVBUZZJ3JTBO6BTOXUATXUR',
'QOS9XD7PSPCSELHGF0MZFSYJHGAWNQDI',
'MEMS7YQUJOKUJZLGMJVBC6DAB7JENECA',
'7KQUQME55MKFOJHJAVF11F2XPWGKUEBV',
'P1D3WEZVS98BGZFXLBHDVJU4BFUYE2RG']
invalid_accounts_sql = "'" + "', '".join(invalid_accounts) + "'"

#充值提现结果
#{ 币种 : { 币种, 充值量, 充值人数, 提现量, 提现人数, 净值 } }
recharge_draw_results = {}

asset_deposit_key = 'Deposit' #充值
asset_withdraw_key = 'Withdraw' #提现

try:
    select_all_sqls = []
    for index in range(1):
        select_all_sql = "SELECT account, qty, balanceType, asset " \
                         "FROM BalanceTransactionData_{INDEX} " \
                         "WHERE date_format(sendingTime, '%Y-%m-%d')='{TODAY}'"\
            .format(INDEX=index, TODAY='2018-11-09') #time.strftime("%Y-%m-%d", time.localtime())
        print(select_all_sql)
        select_all_sqls.append(select_all_sql)

    select_all_union_sql = " union all ".join(select_all_sqls)
    print(select_all_union_sql)

    sql = "SELECT sum(qty), count(DISTINCT account), balanceType, asset " \
          "FROM ({RESULTS})UNION_RESULTS_TABLE " \
          "WHERE account " \
          "NOT IN ({ACCOUNTS}) " \
          "GROUP BY balanceType, asset;"\
        .format(RESULTS=select_all_union_sql, ACCOUNTS=invalid_accounts_sql)
    print(sql)

    # db = MySQLdb.connect("10.5.8.229", "dbanalysis", "dbanalysis@Gdm+110", "orderdata")
    db = pymysql.connect("localhost", "root", "123456", "BitMax")
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    for result in results:
        qty_sum = result[0]
        account_count = result[1]
        balance_type = result[2]
        asset = result[3]
        print("Qty Sum: {0}, Account Count: {1}, Balance Type: {2}, Asset: {3}"\
            .format(qty_sum, account_count, balance_type, asset))

        if asset in recharge_draw_results.keys():
            recharge_draw_result = recharge_draw_results[asset]
        else:
            recharge_draw_result = {'币种': asset}
            recharge_draw_results[asset] = recharge_draw_result

        if balance_type is asset_deposit_key:
            recharge_draw_result['充值量'] = qty_sum
            recharge_draw_result['充值人数'] = account_count
        else:
            recharge_draw_result['提现量'] = qty_sum
            recharge_draw_result['提现人数'] = account_count

    for recharge_draw_result in recharge_draw_results.values():
        if '充值量' not in recharge_draw_result.keys():
            recharge_draw_result['充值量'] = 0
            recharge_draw_result['充值人数'] = 0

        if '提现量' not in recharge_draw_result.keys():
            recharge_draw_result['提现量'] = 0
            recharge_draw_result['提现人数'] = 0

        recharge_draw_result['净值'] = recharge_draw_result['充值量'] - recharge_draw_result['提现量']

except Exception as e:
    print('str(Exception):\t', str(Exception))
    print('str(e):\t\t', str(e))
    print('repr(e):\t', repr(e))
    print('e.message:\t', e.message)
    print('traceback.print_exc():')
    traceback.print_exc()
    print('traceback.format_exc():\n%s' % traceback.format_exc())
    exit(1)

image_path = "/Users/LiXiangYu/Desktop/text11111.jpg"
Imager.data2jpg(list(recharge_draw_results.values()),
                ['币种', '充值量', '充值人数', '提现量', '提现人数', '净值'],
                image_path)
# def mail(receivers=[], subject='Test', content='Test email', image_path=''):
email_receivers = ['1198030047@qq.com']
email_subject = "%s 充值提现" % time.strftime("%Y-%m-%d", time.localtime())
email_content = "这里可以添加邮件内容"
image_path
Emailer.mail(email_receivers, email_subject, email_content, image_path)
