import xlwings as xw
import datetime

from django.conf import settings

from apps.worktable.models import WorkOrderLog


def get_data(date):
	date = datetime.datetime.strptime(date, '%Y-%m')
	work_order_log = WorkOrderLog.objects.filter(
		record_type='create',
		record_time__year=date.year,
		record_time__month=date.month)
	data = []

	for item in work_order_log:
		form_type = item.record_obj.num[0]
		if form_type == 'A':
			num = str(item.record_obj),
			propose_time = item.record_time.strftime("%Y-%m-%d %H:%I"),
			proposer = str(item.record_obj.proposer),
			content = item.record_obj.content,
			state = item.record_obj.get_state_display(),
			types = item.record_obj.get_type_display(),
			try:
				process_record = WorkOrderLog.objects.filter(record_obj=item.record_obj, record_type='process').last()
				processor = str(process_record.recorder)
				process_time = process_record.record_time.strftime("%Y-%m-%d %H:%I")
			except AttributeError:
				processor = None
				process_time = None
			data.append([num, propose_time, proposer, content, processor, process_time, types, state])
	return data


def get_excel(date):
	data = get_data(date)

	# 设为程序可见，不新建工作簿
	# app = xw.App(visible=True, add_book=False)

	# 新建文档，保存
	# wb = xw.Book()
	# wb.save(settings.MEDIA_ROOT + "\\export\\{}.xls".format(file_name))

	# 打开已有文档
	wb = xw.Book(settings.MEDIA_ROOT + "\\export\\template.xls")
	# 进入第一张工作表
	sht0 = wb.sheets[0]

	# 取单元格值
	# value = sht0.range('A1').value

	# 获取已打开的文档名
	# wb = xw.books.active

	# 取列表值
	# list_value = sht0.range('A1:B2').value

	# 批量写入，从左上角 A1 开始
	head = "Daily Jobs Report {}".format(date)
	sht0.range('A1').value = head

	a1 = sht0.range('A1')
	a1.api.Font.Size = 16
	a1.api.Font.Bold = True

	sht0.range('A3').value = data
	# 获取最后列，但是因为第一行合并过，获取的列数不对。
	# last_column = sht0.range(1, 1).end('right').get_address(0, 0)[0]
	last_column = 'H'
	# 获取最后行
	last_row = sht0.range(1, 1).end('down').row
	# 生成表格的数据范围
	table_range = f'A3:{last_column}{last_row}'
	sht0.range(table_range).api.Borders(8).LineStyle = 1 	# 上边框
	sht0.range(table_range).api.Borders(9).LineStyle = 1 	# 下边框
	sht0.range(table_range).api.Borders(7).LineStyle = 1 	# 左边框
	sht0.range(table_range).api.Borders(10).LineStyle = 1 	# 右边框
	sht0.range(table_range).api.Borders(12).LineStyle = 1 	# 内横边框
	sht0.range(table_range).api.Borders(11).LineStyle = 1 	# 内纵边框

	# 写入列有两种方法
	# sht0.range('A1').options(transpose=True).value = [1, 2, 3, 4]
	# titles = [[1], [2], [3], [4]]

	# 批量插入单元格，和插入数据
	'''
	for i in range(5):
		sht0.range('a1:h1').api.Insert()
		sht0.range('a1').value = titles
	'''
	# 保存，关闭，结束进程
	file_name = "Daily Jobs Report {}".format(date)
	file_path = settings.MEDIA_ROOT + "\\export\\{}.xls".format(file_name)
	wb.save(file_path)
	wb.close()
	# app.quit()

	# 返回文件绝对路径
	# path = wb.fullname

	# 返回文件名
	# filename = wb.name

	# 清除 sheet 的内容和格式
	# sht0.clear()

	# 加入超链接
	# a1 = xw.Range('A1')
	# a1.add_hyperlink(r'www.baidu.com', '百度', '提示：点击即链接到百度')

	# 获取超链接
	# hyperlink = a1.add_hyperlink

	# 清除单元格的内容
	# a1.clear()

	# 取得单元格的背景色，以元组形式返回 RGB 值
	# color = a1.color

	# 设置单元格的颜色
	# a1.color = (255, 255, 255)

	# 清除单元格的背景色
	# a1.color = None

	#  获取公式或者输入公式
	# formula = a1.formula
	# formula = a1.formula = '=SUM(B1:B9)'

	# 获得单元格列宽
	# column_width = a1.column_width

	# 新建工作簿，sheet
	# xw.books.add()
	# xw.sheet.add()
	return file_name, file_path
