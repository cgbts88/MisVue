import os
import re
import time
import random

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class FileStorage(FileSystemStorage):

	def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
		super(FileStorage, self).__init__(location, base_url)

	# 重写 _save方法
	def _save(self, name, content):
		# 文件扩展名
		extension = os.path.splitext(name)[1]
		# 文件目录
		dir_name = os.path.dirname(name)
		# 定义文件名，年月日时分秒随机数
		time_stamp = time.strftime('%Y%m%d%H%M%S')
		file_name = time_stamp + '_%d' % random.randint(0, 10)
		# 重写合成文件名
		name = os.path.join(dir_name, file_name + extension)
		# 调用父类方法
		return super(FileStorage, self)._save(name, content)


def format_user_name(name):
	"""
	格式化英文姓名
	将带有空格的英文名称转了全小写不带空格
	"""

	name = name.strip()  # 去除两边空格
	username = ""
	en_name = ""
	for i, item in enumerate(name):
		if i == 0:
			username = item.lower()
			en_name = item
		elif item.isspace():
			en_name += " "
		else:
			username += item.lower()
			en_name += item
	return username, en_name


def form_invalid_msg(form):
	pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
	errors = str(form.errors)
	form_errors = re.findall(pattern, errors)
	ret = {
		'error':  form_errors[0],
		}
	return ret