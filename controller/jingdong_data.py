import pymysql
import requests
import json
# connection = pymysql.connect(host="39.103.215.119",
#                                  port=3308,
#                                  user="zhangjian",
#                                  passwd="Lingxi@123",
#                                  db="ods_outbound_call_platform",
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#
# dm_url = "http://8.142.85.77:8630/report/getDetailedRecord?sessionId={}&workSpaceId=187"
#
# def get_heshen_data(file_name):
#     with open(file_name, 'r') as f:
#         session_ids = f.read()
#
#     dm_texts = []
#     for session_id in session_ids.split("\n"):
#         dm_text = json.loads(requests.get(dm_url.format(session_id)).text)
#         for t in dm_text['result']:
#             data = session_id + "," + t['speakerType'] + "," + t['msgContent']
#             dm_texts.append(data)
#
#     print("read finish")
#
#     with open("未确认本人对话记录.csv",'w') as f:
#         f.write("sessionId, 角色, 话术\n")
#         for d in dm_texts:
#             f.write(d)
#             f.write("\n")
#
#
# def get_id_and_repay(customerIds):
#     connection = pymysql.connect(host="39.103.215.119",
#                                  port=3308,
#                                  user="zhangjian",
#                                  passwd="Lingxi@123",
#                                  db="ods_outbound_call_platform",
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     data = []
#     for customer_id in customerIds:
#         sql = "select rs.customer_id as customer_id, rs.id as case_id, occrr.repaid_date as repaid_date, occrr.money as money from ( " \
#                 "select id,customer_id from outbound_call_case  where customer_id = '{}' ) rs " \
#                 "left join outbound_call_case_repaid_record occrr " \
#                 "on rs.id = occrr.case_id ".format(customer_id)
#         print(sql)
#         cursor = connection.cursor()
#         cursor.execute(sql)
#         rs = cursor.fetchall()
#         data.extend(rs)
#     # for r in rs:
#     #     data.append([r["case_id"], r["repaid_date"], r['money']])
#
#     return data
#
# def get_case_id_and_repay(file_name):
#     datas = pd.read_csv(file_name)
#     customerIds = set([])
#     for d in list(datas['jd_pin']):
#         if pd.notna(d):
#             customerIds.add(d)
#     print(customerIds)
#     results = get_id_and_repay(customerIds)
#     datas["case_id"] = datas['jd_pin'].apply(lambda x: handle_id(x, results))
#     datas["repaid_date"] = datas['jd_pin'].apply(lambda x: handle_repay(x, results))
#     datas["money"] = datas['jd_pin'].apply(lambda x: handle_money(x, results))
#
#     datas.to_csv(file_name.replace("csv","_update.csv"), index=False)
#
# def handle_id(x,data):
#     for d in data:
#         if x == d['customer_id']:
#             return d['case_id']
#
#     return pd.NA
#
#
# def handle_repay(x,data):
#     for d in data:
#         if x == d['customer_id']:
#             return d['repaid_date']
#     return pd.NA
#
#
# def handle_money(x,data):
#     for d in data:
#         if x == d['customer_id']:
#             return d['money']
#     return pd.NA
#
#
# def get_outbound_type_by_id(customer_id, phone):
#     connection = pymysql.connect(host="39.103.215.119",
#                                  port=3308,
#                                  user="zhangjian",
#                                  passwd="Lingxi@123",
#                                  db="ods_outbound_call_platform",
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     sql = "select occd.outbound_type as outbound_type "\
# 	" from outbound_call_case_detail occd , outbound_call_case occ "\
# 	" where occd.case_id = occ.id and occd.phone_number = '{}' " \
#           "and occ.customer_id = '{}'".format(phone, customer_id)
#     print(sql)
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     rs = cursor.fetchall()
#     if len(rs) > 0:
#         return rs[0]['outbound_type']
#     else:
#         return -1
#
#
# def get_outbound_type(file_name):
#     datas = pd.read_csv(file_name)
#
#     for index,row in datas.iterrows():
#         phone = row['手机号']
#         customer_id = row["customer_id"]
#         datas["是否本人"] = get_outbound_type_by_id(customer_id, phone)
#
#     datas.to_csv(file_name.replace(".csv","_new.csv"), index=False)
import tqdm


def get_complain(start_time, end_time):
    connection = pymysql.connect(host="39.103.215.119",
                                 port=3308,
                                 user="zhangjian",
                                 passwd="Lingxi@123",
                                 db="ods_outbound_call_platform",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # sql = "select call_case_id, dm_session_id, id from " \
    #       "outbound_call_result where intent_id = 10083 " \
    #       "and call_start_time > '{}' and call_end_time < '{}' " \
    #       "and call_status in ('normalConnection' , 'dmError', 'dmTimeOut') ".format(start_time, end_time)

    sql = "select t.dm_session_id, t.call_case_id, t.answer_time from (select id from outbound_call_case where intent_id = 10083) rs, " \
          "outbound_call_result t, outbound_call_collection_result c " \
          "where rs.id = t.call_case_id and t.id = c.id and t.call_status = 'normalConnection' and t.call_type = 3 and t.call_start_time >= '{}' " \
          "and t.call_start_time <= '{}' and c.authentication in {} and t.state = 10 ".format(start_time,
                                                                                                      end_time, 1)
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    print(len(datas))
    complain_data = []
    complain_str = ""
    index = 1
    # dm_url = "http://172.26.2.56:8636/report/getDetailedRecord/?sessionId={}"
    # dm_url = "http://8.142.85.77:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    dm_url = "http://172.26.2.56:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    for data in tqdm.tqdm(datas):
        print("handle [{}]".format(index))
        print(dm_url.format(data["dm_session_id"]))
        try:
            dm_content_json = json.loads(requests.get(dm_url.format(data["dm_session_id"])).text)
            # dm_content_json = json.loads(requests.get(dm_url.format("32439076444651957516612169040524724")).text)
            labels = []
            for d in dm_content_json['result']:
                if d['msgContent'] and ("欠了多少钱" in d['msgContent'] and "F121" in d['msgContent']):
                    complain_data.append("{},{},{}".format(data['dm_session_id'],
                                                           data["call_case_id"], d["msgContent"]))
                    complain_str = "{},'{}'".format(complain_str, data['dm_session_id'])
                    break
            index = index + 1
        except Exception as e:
            print("{} not get dm context".format(data["dm_session_id"]))

    # print(complain_data)
    print(complain_str)
    with open("{}_complain.txt".format("25-29"), 'a+') as f:
        f.write(complain_str)
        # for da in complain_data:
        #     f.write(da)
        #     f.write("\n")


if __name__ == "__main__":
    # file_name = "未确认本人-session.txt"
    # get_heshen_data(file_name)
    # file_name = "collection_message.csv"
    # get_case_id_and_repay(file_name)
    # get_outbound_type(file_name)
    import datetime
    import threading
    start_time = "2022-10-01 00:00:00"
    end_time = "2022-10-31 23:59:59"
    thread_list = []
    for i in range(0, 1):
        print(start_time)
        print(end_time)

        t1 = threading.Thread(target=get_complain, args=(start_time, end_time))
        t1.start()
        thread_list.append(t1)
        start_time = (datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    for t in thread_list:
        t.join()



