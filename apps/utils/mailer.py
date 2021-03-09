import os
import threading
import smtplib
import ssl
from datetime import datetime

from loguru import logger

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header

from apps.asset.models import NetworkDevice, AssetOrder, Stock
from apps.users.models import Department
from apps.worktable.models import WorkOrder, WorkOrderLog

from utils.export import get_excel


class EmailThread(threading.Thread):
    _sender_email = "robot@qsmfg.com"
    _password = "Ewig@2021"

    def __init__(self, subject, body, from_email, to, fail_silently, cc=None, attachments=None):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = to
        self.fail_silently = fail_silently
        self.cc = cc
        self.attachments = attachments
        threading.Thread.__init__(self)

    @staticmethod
    def __format_addr__(addr):
        # 解析邮件地址，以保证邮件别名可以显示
        alias_name, email_addr = parseaddr(addr)
        # 防止中文问题，进行转码处理，并格式化为 str 返回
        return formataddr((alias_name, email_addr))

    def run(self):
        str_to_list = list()
        try:
            for item in self.to:
                str_to_list.append(self.__format_addr__(item))
        except TypeError:
            str_to_list = self.to
        message = MIMEMultipart("alternative")
        message['Subject'] = Header(self.subject)    # Subject format by Header
        message['From'] = self._sender_email
        message['To'] = ','.join(str_to_list)    # Receiver must be String
        if self.cc:
            message['Bcc'] = self.__format_addr__(self.cc)
        if self.attachments:
            with open(self.attachments, 'rb') as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                file_name = os.path.basename(self.attachments)
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=file_name,
                )
                message.attach(part)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.body, 'plain')
        part2 = MIMEText(self.body, 'html')

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, context=context) as server:
                server.login(self._sender_email, self._password)
                server.sendmail(
                    self._sender_email, str_to_list, message.as_string()
                )
        except Exception as error:
            logger.add("media\\log\\{}.log".format(datetime.now().strftime("%Y%m%d-%H%M")))
            logger.error(error)


def send_work_order_message(num):
    work_order = WorkOrder.objects.get(num=num)

    from_email = 'Robot<robot@qsmfg.com>'
    edp_mail = 'chengeng@qsmfg.com'    # 'DGEDP<dgedp@qsmfg.com>'
    proposer_mail = "{0}<{1}>".format(work_order.proposer, work_order.proposer.email)

    content = ''
    processor_mail = ''
    to = []

    fail_silently = True

    try:
        work_order_log = WorkOrderLog.objects.filter(record_obj=work_order, record_type='process').last()
        processor_mail = "{0}<{1}>".format(work_order_log.recorder, work_order_log.recorder.email)
    except AttributeError:
        work_order_log = None

    if work_order_log:
        if work_order.state == 'process':
            content = "工單 {0} 已經由【 {1} 】跟進處理。".format(work_order.num, work_order_log.recorder)
            to = [edp_mail, proposer_mail]
        elif work_order.state == 'finish':
            content = "工單 {0} 已經由【 {1} 】處理完畢，請點擊以下工單號關閉工單。".format(work_order.num, work_order_log.recorder)
            to = [processor_mail, proposer_mail]
        elif work_order.state == 'confirm':
            to = [processor_mail]
    else:
        content = ""
        to = [edp_mail, proposer_mail]

    subject = "{0}　{1}".format(work_order.num, work_order.get_state_display())
    body = r"""
    <h3>{0}</h3>
    <p>申請單號：<a href="http://192.1.2.99/worktable/order/detail/?num={1}">{1}</a></p>
    <p>發起時間：{2}</p>
    <p>使用人：{3}</p>
    <p>分機號：{4}</p>
    <p>E-Mail：<a href="mailto:{5}">{5}</a></p>
    <p>附件：<a href="http://192.1.2.99/media/{6}">{6}</a></p>
    <p>狀態：{7}</p>
    <p>IP地址：{8}</p>
    <pre>問題描述：{9}</pre>
    """.format(
        content,
        work_order.num,
        WorkOrderLog.objects.get(record_obj=work_order, record_type='create').record_time.strftime("%Y-%m-%d %H:%I"),
        work_order.proposer,
        work_order.proposer.ext_num,
        work_order.proposer.email,
        '',        # work_order.attachment,
        work_order.get_state_display(),
        NetworkDevice.objects.get(asset_user_id=work_order.proposer).ip,
        work_order.content,
    )
    EmailThread(subject, body, from_email, to, fail_silently).start()


def send_asset_order_message(num):
    asset_order = AssetOrder.objects.get(num=num)
    target_department = Department.objects.get(simple_title=asset_order.target_department)

    from_email = 'Robot<robot@qsmfg.com>'
    acc_mail = "Zou Lai Hong (鄒來紅)<zoulaihong@qsmfg.com>"
    edp_mail = 'DGEDP<dgedp@qsmfg.com>'
    try:
        target_clerk_mail = "{0}<{1}>".format(target_department.clerk, target_department.clerk.email)
        to = [edp_mail, target_clerk_mail]
    except AttributeError:
        to = [edp_mail]
    try:
        target_asset_owner_mail = "{0}<{1}>".format(target_department.asset_owner, target_department.asset_owner.email)
        cc_list = [acc_mail, target_asset_owner_mail]
    except AttributeError:
        cc_list = [acc_mail]

    fail_silently = True

    edp_content = ''
    for edp_asset_item in asset_order.edp_asset.split(','):
        edp_stock_obj = Stock.objects.get(edp_num=edp_asset_item)
        edp_stock_content = r"""
        <p>　　　　　<b>類型：</b>{0}　<b>型號：</b>{1}　<b>ACC編號：</b>{2}　<b>EDP編號：</b>{3}</p>
        """.format(
            edp_stock_obj.model.type.cn_code,
            edp_stock_obj.model,
            edp_stock_obj.acc_num,
            edp_stock_obj.edp_num,
        )
        edp_content += edp_stock_content

    target_content = ''
    for target_asset_item in asset_order.target_asset.split(','):
        target_asset_obj = Stock.objects.get(edp_num=target_asset_item)
        target_stock_content = r"""
        <p>　　　　　<b>類型：</b>{0}　<b>型號：</b>{1}　<b>ACC編號：</b>{2}　<b>EDP編號：</b>{3}</p>
        """.format(
            target_asset_obj.model.type.cn_code,
            target_asset_obj.model,
            target_asset_obj.acc_num,
            target_asset_obj.edp_num,
        )
        target_content += target_stock_content

    subject = "{0}　{1}".format(asset_order.num, "资产转移")
    body = r"""
    <p>申請單號：<a href="http://192.1.2.99/asset/order/detail/?num={0}">{0}</a></p>
    <p>發起時間：{1}</p>
    <p>EDP轉出：{2}</p>
    <p>{3}轉出：{4}</p>
    """.format(
        asset_order.num,
        asset_order.transfer_time.strftime("%Y-%m-%d %H:%I"),
        edp_content,
        target_department.simple_title,
        target_content,
    )
    EmailThread(subject, body, from_email, to, fail_silently, cc=cc_list).start()


def send_daily_job_excel(month):
    file_name, file_path = get_excel(month)
    fail_silently = True
    body = ''
    from_email = 'Robot<robot@qsmfg.com>'
    to = ['DGEDP<dgedp@qsmfg.com>']
    EmailThread(file_name, body, from_email, to, fail_silently, attachments=file_path).start()
