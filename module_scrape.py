from selenium import webdriver
import pandas as pd
from bs4 import SoupStrainer,BeautifulSoup
import numpy as np
import time	
import re
import pickle

driver = webdriver.Chrome("chromedriver.exe")
driver.get('https://www.genome.jp/kegg-bin/get_htext?ko00002.keg')

time.sleep(1)
# try:
time.sleep(5)
element = driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td/a[3]")
element.click()
tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')
table = tutorial_soup.find( "table", {"id":"grid"} )
names = table.find_all("td",{"colspan":1})
# print(names)
h_name = []
tag = []
for n in names:
	tag.append(re.sub(r'\d+',"",n.find("a")['name']))
	h_name.append(n.text.strip().replace("\n",''))
print(len(h_name))
print(len(tag))


element= driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td/a[4]/img")
element.click()
tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')
table = tutorial_soup.find( "table", {"id":"grid"} )
mini_tables = table.find_all("td",{"class":"col1"})
print(len(mini_tables))
h1_index = 0
h2_index = 1
h3_index = 2
index = 0

h1_names = []
h2_names = []
h3_names = []

m_num=[]
m_name =[]
m_sm = []

link="https://www.genome.jp/kegg-bin/show_module?"
for i in mini_tables[1:]:
	print(tag[h1_index],tag[h2_index],tag[h3_index])
	print(h_name[h1_index])
	print(h_name[h2_index])
	print(h_name[h3_index])

	h1_name = h_name[h1_index]
	h2_name = h_name[h2_index]
	h3_name = h_name[h3_index]

	pre = i.find("pre")
	split_text = pre.text.split("\n")

	if split_text[0] == '\xa0':
		pass

	else:
		for i in split_text[:len(split_text)-1]:

			stp = i.strip()
			m_num.append(stp[:7])
			m_name.append(stp[7:stp.find("[P")])
			m_sm.append(stp[stp.find("[P"):])

			h1_names.append(h1_name)
			h2_names.append(h2_name)
			h3_names.append(h3_name)	

		if h3_index == 59:
			break

		if tag[h3_index] == 'C' and tag[h3_index + 1] == 'C':
			h3_index = h3_index+1
		elif tag[h3_index] == 'C' and tag[h3_index + 1] == 'B':
			h2_index = h3_index+1
			h3_index = h3_index+2
		elif tag[h3_index] == 'C' and tag[h3_index + 1] == 'A':
			h1_index = h3_index+1
			h2_index = h3_index+2
			h3_index = h3_index+3
		else:
			pass

df = pd.DataFrame.from_dict({"h1 name": h1_names,"h2 name": h2_names,"h3 name": h3_names, "Module_Number":m_num,"Module_name":m_name,"Associations":m_sm})
print(df[["h1 name","h2 name", "h3 name", "Module_Number"]].head(200))
with open("scraped.pkl","wb") as f:
	pickle.dump(df,f)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
df_ko = []
for i in m_num:
	try:
		print(i)
		time.sleep(5)
		driver.get(link+ str(i))
		ko = driver.find_element_by_xpath("//*[@id='definition']/table/tbody/tr[3]/td[2]")
		kos = ko.text.replace("\n",",").replace("(","").replace(")","").replace(" ",",")
		print(kos)
		df_ko.append([kos])
		time.sleep(3)

	except:
		df_ko.append(["Not available"])

df_2 = pd.DataFrame.from_dict({"Module_Number":m_num,"KO's":df_ko})
with open("scraped2.pkl","wb") as f:
	pickle.dump(df_2,f)





# 	for i in mini_tables:
# 		m_num=[]
# 		m_name =[]
# 		m_sm = []
# 		pre = i.find("pre")
# 		split_text = pre.text.split("\n")
# 		for i in split_text:
# 			stp = i.strip()
# 			m_num.append(stp[:7])
# 			m_name.append(stp[7:stp.find("[P")])
# 			m_sm.append(stp[stp.find("[P"):])
# 	result = tutorial_soup.find_all('a')
# 	print(result)
# 	print(element)

# except Exception as e:
# 	print(e)





# A1 - //*[@id="grid"]/tbody/tr[1]/td/pre/b
# //*[@id="grid"]/tbody/tr[1]/td/pre/a[2]
# //*[@id="grid"]/tbody/tr[1]/td/pre/a[1]
# //*[@id="grid"]/tbody/tr[1]/td/pre/a[

# B1- //*[@id="grid"]/tbody/tr[3]/td/pre/b
# //*[@id="grid"]/tbody/tr[3]/td/pre/a[2]