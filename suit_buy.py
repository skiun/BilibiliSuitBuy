# -*- coding:utf-8 -*-

# https://github.com/lllk140

from requests.utils import cookiejar_from_dict
from urllib.parse import urlencode
import requests
import hashlib
import time
import uuid


"""

没有异常处理可言, 网络不行直接死, 你都开脚本了不求快? 求稳? 演别开, 开别演。

啊, 注释是什么

报错建议直接百度, 都是调用调用的, 百度一查, 自己再看报错的行数, 一步一步推上去就行

有问题问了没回, 那可能是在rundown7坐牢 等几个小时就行了

测试过1次, 26134失败, 不想送钱啦, 摆烂了, 一起烂吧

"""


class BuyConfig:
    cookie_text = ""  # fiddler抓包
    app_sec = "560c52ccd288fed045859ed18bffd973"  # fiddler抓包
    access_key = ""  # fiddler抓包
    buv_id = ""  # fiddler抓包
    app_key = ""  # fiddler抓包
    item_id = ""  # fiddler抓包
    phone = ""  # fiddler抓包
    system = ""  # fiddler抓包
    channel = ""  # fiddler抓包
    sdk_int = ""  # fiddler抓包
    add_month = "-1"  # 字面意思
    buy_num = "1"  # 字面意思
    coupon_token = ""  # 字面意思
    jump_time: int = 3  # 字面意思


class ToolsRequests:
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"}

    def __init__(self):
        """
        嗯, 嗯, 嗯, 很简单的调用, 具体是啥也不需要晓得😄
        """
        self.request = requests.Session()
        self.request.headers = self.header

    def _GetAppVersion(self, mobi_app="android"):
        """
        呃, 呃, 呃, 很简单的网络请求, 具体获取app最新的版本号🥺
        """
        url, params = "https://app.bilibili.com/x/v2/version", {"mobi_app": mobi_app}
        response = self.request.get(url, params=params)
        app_data = response.json()['data'][0]
        return str(app_data['build']), str(app_data['version'])
        # return "", "6.72.0"

    def _GetSuitData(self, zb_id):
        """
        懂的都懂😋
        """
        url, params = "https://api.bilibili.com/x/garb/v2/mall/suit/detail", {"item_id": zb_id}
        response = self.request.get(url, params=params)
        sale_time = response.json()["data"]["properties"]["sale_time_begin"]
        suit_name = response.json()["data"]["name"]
        return str(suit_name), int(sale_time)

    def _GetBiliNowTime(self, *args, **kwargs):
        """
        不是说没有异常处理的吗。怎么辉石呢, 是啊, 怎么辉石呢.jpg
        """
        url = "http://api.bilibili.com/x/report/click/now"
        try:
            response = self.request.get(url, timeout=0.5)
        except Exception as e:
            self._GetBiliNowTime(e)
        else:
            return int(response.json()['data']['now'])


class BuyRequests(BuyConfig, ToolsRequests):
    def __init__(self):
        """
        摆烂了, 能用就行, 乱一点就乱一点吧🥰
        """
        super().__init__()
        self.cookie = self._CookieConvertDict()
        self.sale_time = self._GetSuitData(self.item_id)[1]
        # self.sale_time = round(time.time()) + 10
        build, version = self._GetAppVersion()

        self.data = self._GenerateData(version)
        self.buy_request = requests.Session()
        self.buy_request.cookies = cookiejar_from_dict(self.cookie)
        self.buy_request.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "User-Agent": self._GenerateAgent(build, version),
            "Content-Length": str(len(self.data)),
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "APP-KEY": "android64", "env": "prod", "native_api_from": "h5",
            "Referer": f"https://www.bilibili.com/h5/mall/suit/detail?id={self.item_id}&navhide=1",
            "x-bili-aurora-eid": "", "x-bili-aurora-zone": "", "x-bili-mid": f"{self.cookie['DedeUserID']}",
            "x-bili-trace-id": self._GenerateTraceId(), "Connection": "keep-alive", "Host": "api.biliapi.net"
        }
        print(self.data)
        print(self.buy_request.cookies)
        print(self.buy_request.headers)

    def _CookieConvertDict(self):
        """ 没让你们一个一个复制cookie的key和value, 很人性化吧 😁 """
        """ 格式直接从fiddler复制 """
        cookie_str = self.cookie_text.replace(" ", "")[7:]
        cookie_list = [tuple(li.split("=")) for li in cookie_str.split(";")]
        return {key: value for key, value in cookie_list}

    def _GenerateAgent(self, build, version):
        """ 呦,啊 """
        user_agent_list = [
            f"Mozilla/5.0 (Linux; Android {self.system}; {self.phone} Build/OPR1.170623.027; wv) AppleWebKit/537.36",
            f"(KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36",
            f"os/android model/{self.phone} build/{build} osVer/{self.system} sdkInt/{self.sdk_int} network/2",
            f"BiliApp/{build} mobi_app/android channel/{self.channel} Buvid/{self.buv_id}",
            f"innerVer/{build} c_locale/zh_CN s_locale/zh_CN disable_rcmd/0 {version} os/android model/{self.phone}",
            f"mobi_app/android build/{build} channel/{self.channel} innerVer/{build} osVer/{self.system} network/2"
        ]
        return " ".join(user_agent_list)

    def _GenerateDataMd5(self, data_str):
        """ 我的评价是md5 """
        md5_data = f"{data_str}{self.app_sec}"
        md5_ = hashlib.md5()
        md5_.update(md5_data.encode())
        return md5_.hexdigest()

    def _GenerateData(self, version):
        """ 万恶的表单 """
        statistics = '{"appId":1,"platform":3,"version":"__version__","abtest":""}'
        data_str = urlencode({
            "access_key": self.access_key,
            "add_month": self.add_month,
            "appkey": self.app_key,
            "buy_num": str(self.buy_num),
            "coupon_token": str(self.coupon_token),
            "csrf": self.cookie["bili_jct"],
            "currency": "bp",
            "disable_rcmd": "0",
            "item_id": str(self.item_id),
            "platform": "android",
            "statistics": statistics.replace("__version__", version),
            "ts": str(self.sale_time)
        })
        sign = self._GenerateDataMd5(data_str)
        return data_str + f"&sign={sign}"

    def _GenerateTraceId(self):
        """ 我的评价是2个字: 抄的。 具体哪抄的忘了 😘 """
        a, b = "".join(str(uuid.uuid4()).split("-")), hex(int(self.item_id))
        return a[0:26] + b[2:8] + ":" + a[16:26] + b[2:8] + ":0:0"

    def _SuitBuy(self, test=True):
        """ 万恶头子 """
        url = "https://api.bilibili.com/x/garb/v2/trade/create"
        if test:
            print("run request ok")
        else:
            response = self.buy_request.post(url, data=self.data)
            print(response.text)


class SuitBuy(BuyRequests):
    def WaitLocalTime(self):
        """ 你看看函数名 👀 """
        jump_time_ = self.sale_time - self.jump_time
        now_time = time.time()
        print(jump_time_, self.sale_time)
        while jump_time_ >= now_time:
            time.sleep(0.001)
            now_time = time.time()
            print(f"\r{jump_time_ - now_time}", end="")

    def WaitSeverTime(self):
        """ 你看看函数名 👀 """
        while True:
            s = time.time()
            bili_time = self._GetBiliNowTime()
            if bili_time >= self.sale_time:
                return True
            time.sleep(0.05)
            e = time.time()
            print(bili_time, e - s)

    def start(self, test=True):
        """ test=False == run """
        self.WaitLocalTime()
        self.WaitSeverTime()
        self._SuitBuy(test)
        input(">>>>>>>>>")


if __name__ == '__main__':
    ss = time.time()
    Buy = SuitBuy()
    ee = time.time()
    print("准备耗时:", ee - ss)
    Buy.start(True)
