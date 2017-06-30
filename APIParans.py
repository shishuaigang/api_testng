# -*- coding: utf-8 -*-
import csv
import os
import codecs
import json
import sys
import platform

reload(sys)
sys.setdefaultencoding('utf8')


class api_num:
    def __init__(self, _path):
        self.path = _path

    @property
    def json_data(self):
        for files in os.walk(self.path):
            json_file = files[2]
        return [f for f in json_file if f.endswith(".json")]

    def read_section(self):  # 返回每个section下value的值
        os.chdir(self.path)
        re = []
        temp = [(json.loads(codecs.open(self.json_data[i], encoding='utf-8').read()))["section"]
                for i in range(len(self.json_data))]  # 结构[[{},{},{}],[{}]]
        for i in range(len(self.json_data)):
            result = []
            for j in range(len(temp[i])):
                result.append(temp[i][j]['value'])  # i=0时，result的第一个元素插入了temp[i]下面的所有value的值
            re.append(result)
        return re

    def every_json_api_number(self):  # 每个json文件下有多少个API，存入list
        # 返回格式[[15], [27, 6, 4, 3, 6, 5, 3, 8, 4, 3, 18, 6, 6], [63], [38]]
        os.chdir(self.path)
        l = self.read_section()
        re = []
        for i in range(len(self.json_data)):
            result = []
            for j in range(len(l[i])):
                result.append(len(json.loads(codecs.open(self.json_data[i], encoding='utf-8').read())[l[i][j]]))
            re.append(result)
        return re


class api_url(api_num):
    def api_url(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        url = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):  # num[m]是一个list
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                                "NoNeed"] == str(0):
                            url.append(dict_json[array_name[m][n]][k]["url"])
        return url


class api_cn_name(api_num):
    def api_chinese_name(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        api_chinese_name = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                                "NoNeed"] == str(0):
                            api_chinese_name.append(dict_json[array_name[m][n]][k]["summary"])  # api的中文名字
        return api_chinese_name


class api_cor_params(api_url):
    def api_details(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        param_all_details = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                                "NoNeed"] == str(0):
                            param_all_details.append(dict_json[array_name[m][n]][k]["params"])
        return param_all_details

    def api_correct_params(self):
        params = []
        api_param_details = self.api_details()
        for i in range(len(self.api_url())):
            st = ""
            for j in range(len(api_param_details[i].keys())):
                st = st + (
                    api_param_details[i].keys()[j] + "=" + str(api_param_details[i].values()[j]["default"]) + "&")
            params.append(st + "APIVersion=999999999")
        return params


class write_param(api_url, api_cor_params):
    def writeCSV(self):

        API_URL = self.api_url()
        PARAMS = self.api_correct_params()
        if platform.system() == "Darwin":
            os.chdir(r"E:\Original_code\api_testng")
        elif platform.system() == "Windows":
            os.chdir("/Users/shishuaigang/PycharmProjects/api_testng")
        with open('APIparam.csv', 'wb') as csvfile:
            temp = csv.writer(csvfile, dialect='excel')
            for i in range(len(API_URL)):
                temp.writerow([API_URL[i], PARAMS[i]])

if __name__ == "__main__":
    path_windows = r"E:\test\inroad"
    path_mac = "/Users/shishuaigang/Desktop/Auto_test/testjson"
    print api_num(path_mac).json_data
    print api_num(path_mac).read_section()
    print platform.system()
    '''
    if platform.system() == "Darwin":
        write_param(path_mac).writeCSV()
    elif platform.system() == "Windows":
        write_param(path_windows).writeCSV()
'''