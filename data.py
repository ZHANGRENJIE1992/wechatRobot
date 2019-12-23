import pandas as pd

def handle_rawdata_groupname(rawdata):
	groupname=[] #分离出所有群
	for raw in rawdata:
		GroupName = raw['GroupName']
		groupname.append(GroupName)
		#groupname = set(groupname)
	groupname = set(groupname)
	return groupname

def groupchatcontentbygroupname(groupname,rawdata):
	df = pd.read_excel('robot_config.xlsx', sheet_name='QA')
	questions = list(df['Q'])
	groupActiveId = []
	export_dataset = []
	export_data = {}
	metaData = []
	contentGroup = []
	data1 = []
	data2 = []
	data3 = []
	data4 = []
	data5 = []
	data6 = [] 
	keyword1 = 0
	keyword2 = 0
	keyword3 = 0
	keyword4 = 0
	keyword5 = 0
	keyword6 = 0
	keyword7 = 0
	keyword8 = 0
	keyword9 = 0
	keyword10 = 0
	keyword11 = 0
	keywords = [keyword1,keyword2,keyword3,keyword3,keyword4,keyword5,keyword6,keyword7,keyword8,keyword9,keyword10,keyword11]
	timeData1 = {"time":"00:00 - 04:00","data": data1}
	timeData2 = {"time":"04:00 - 08:00","data": data2}
	timeData3 = {"time":"08:00 - 12:00","data": data3}
	timeData4 = {"time":"12:00 - 16:00","data": data4}
	timeData5 = {"time":"16:00 - 20:00","data": data5}
	timeData6 = {"time":"20:00 - 24:00","data": data6}
	for name in groupname:	#分离出对应群的数组
		export_data = {"sheet_name":name,"data":metaData}#每个群内的聊天内容
		
		for raw in rawdata:
			if raw['GroupName'] == name:
				metaData.append(raw)
		export_dataset.append(export_data)
		metaData = []

	for export_data in export_dataset:
		for data in export_data["data"]: #按时间分成6个元素
			#print(data)
			if 0<=data["Time"].hour <4:
				data1.append(data)
			if 4<=data["Time"].hour <8:
				data2.append(data)
			if 8<=data["Time"].hour <12:
				data3.append(data)
			if 12<=data["Time"].hour <16:
				data4.append(data)
			if 16<=data["Time"].hour <20:
				data5.append(data)
			if 20<=data["Time"].hour <24:
				data6.append(data)
		#print("data4",data4)
		export_data["data"] =[timeData1,timeData2,timeData3,timeData4,timeData5,timeData6]
		data1 = []
		data2 = []
		data3 = []
		data4 = []
		data5 = []
		data6 = []
		timeData1 = {"time":"00:00 - 04:00","data": data1}
		timeData2 = {"time":"04:00 - 08:00","data": data2}
		timeData3 = {"time":"08:00 - 12:00","data": data3}
		timeData4 = {"time":"12:00 - 16:00","data": data4}
		timeData5 = {"time":"16:00 - 20:00","data": data5}
		timeData6 = {"time":"20:00 - 24:00","data": data6}
		#print("data4",data4)
	
	for export_data in export_dataset:
		for timedataset in export_data["data"]: #定位到单一时间段
			if timedataset["data"]:
				date = timedataset["data"][0]["Time"].strftime('%Y-%m-%d')
				phase = timedataset["time"]
				groupname = timedataset["data"][0]["GroupName"]
				groupsize = timedataset["data"][0]["GroupSize"]
				for dataID in timedataset["data"]:
					groupactiveid = dataID["WechatID"]
					contengroup = dataID["Content"]
					groupActiveId.append(groupactiveid)
					contentGroup.append(contengroup)
				activeID = set(groupActiveId)
				activeCount = len(activeID)
				activeID = ",".join(map(lambda x:str(x),activeID))
				if contentGroup:
					for content in contentGroup:
						i = 1
						for question in questions:
							if question in content:
								print("zhaodao匹配")
								keywords[i] = keywords[i]+1
							i=i+1
				timedataset["data"] = [date,phase,groupname,groupsize,activeCount,activeID,keywords[1],keywords[2],keywords[3],keywords[4],keywords[5],keywords[6],keywords[7],keywords[8],keywords[9],keywords[10],keywords[11]]


			groupActiveId=[]
			contentGroup =[]
			keyword1 = 0
			keyword2 = 0
			keyword3 = 0
			keyword4 = 0
			keyword5 = 0
			keyword6 = 0
			keyword7 = 0
			keyword8 = 0
			keyword9 = 0
			keyword10 = 0
			keyword11 = 0
			keywords = [keyword1,keyword2,keyword3,keyword3,keyword4,keyword5,keyword6,keyword7,keyword8,keyword9,keyword10,keyword11]
			#print(timedataset["data"])
	return export_dataset



"""class timeClass:
	#单个数据时间段的数组 "日期","时间段","群昵称","群人数","新增人数","活跃数","活跃账号","关键词参观时间出现次数","关键词闭馆时间出现次数","关键词门票出现次数","关键词门票优惠出现次数","关键词团队购票出现次数","关键词免票出现次数","关键词讲解出现次数","关键词地址出现次数","关键词怎么去博物馆出现次数","关键词电话出现次数","关键词发票出现次数"
	date = ""
	phase = ""
	groupname = ""
	groupsize =0
	newaccount = 0
	activeCount = 0
	activeID = []
	keyword1 = 0
	keyword2 = 0
	keyword3 = 0
	keyword4 = 0
	keyword5 = 0
	keyword6 = 0
	keyword7 = 0
	keyword8 = 0
	keyword9 = 0
	keyword10 = 0
	keyword11 = 0
	
	def __init__(self,date,phase,groupname):
		self.timeClass = [date,phase,groupname,groupsize,newaccount,activeCount,activeID,keyword1,keyword2,keyword3,keyword3,keyword4,keyword5,keyword6,keyword7,keyword8,keyword9,keyword10,keyword11]
"""



