__author__ = 'Luzaofa'
__date__ = '2019/7/7 19:28'

import time
import json
import requests


class WeChat(object):
    '''发送企业微信'''

    def __init__(self, user):
        # 参数配置文档：https://work.weixin.qq.com/api/doc#10013
        self.CORPID = 'AAAAA'
        self.CORPSECRET = 'BBBBB'
        self.AGENTID = 'CCCCC'
        self.TOUSER = user  # 接收者用户名

    def _get_access_token(self):
        '''获取access_token'''
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {
            'corpid': self.CORPID,
            'corpsecret': self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        '''保存access_token到本地文件'''
        try:
            with open('token/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except Exception:
            with open('token/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('token/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def get_media_id(self, path):
        '''获取media_id'''
        url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={0}&type=file'.format(
            self.get_access_token())
        files = {'file': open(path, 'rb')}
        req = requests.post(url, files=files)
        data = json.loads(req.text)
        return data["media_id"]

    def send_file(self, message, filepath):
        print('正在给:{0}发信息。'.format(self.TOUSER))
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_data = '{"msgtype": "text", "safe": "0", "agentid": %s, "touser": "%s", "text": {"content": "%s"}}' % (
            self.AGENTID, self.TOUSER, message)
        send_doc = '{"msgtype": "file", "safe": "0", "agentid": %s, "touser": "%s", "file": {"media_id": "%s"}}' % (
            self.AGENTID, self.TOUSER, self.get_media_id(filepath))
        r = requests.post(send_url, send_data)
        if json.loads(r.content)['errmsg'] == 'ok':
            print('提示信息发送成功')
        doc = requests.post(send_url, send_doc)
        if json.loads(doc.content)['errmsg'] == 'ok':
            print('附件发送成功')
        return r.content

    def send_data(self, message):
        '''发送信息'''
        print('正在给:{0}发信息。'.format(self.TOUSER))
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_data = '{"msgtype": "text", "safe": "0", "agentid": %s, "touser": "%s", "text": {"content": "%s"}}' % (
            self.AGENTID, self.TOUSER, message)
        try:
            r = requests.post(send_url, send_data)
            if json.loads(r.content)['errmsg'] == 'ok':
                print('提示信息发送成功')
                return True
            raise Exception
        except Exception:
            return False


if __name__ == '__main__':
    wx = WeChat('Luzaofa')
    # wx.send_data("test")
    wx.send_file("test", './test.txt')
