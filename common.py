import xlwt

class Excel:
    def createExcel(self, title, dataset,name):
        wb = xlwt.Workbook(encoding='utf-8')
        for data in dataset:
	        ws = wb.add_sheet(data["sheet_name"])
	        dataValue = data["data"]
	        n = 0
	        for t in title:
	            ws.write(0, n, t)
	            n += 1
	        i = 1
	        for row in dataValue:
	            j = 0
	            if row["data"]:
		            for val in row["data"]:
		                ws.write(i, j, val)
		                j += 1
		            i += 1
        #fix = ".xls"
        #name = f"{now_str}_{fix}"
        #wb.save(name)
        #return wb
        wb.save(name)