from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import pandas as pd
driver=webdriver.Chrome('./chromedriver.exe')
#driver=webdriver.Chrome('./chromedriver')    #For linux
data=pd.read_csv('data.csv')


for i in range(len(data)): 
	print(f"Data Entry {i}:")
	print(data.iloc[i])
	#-------------------------------------
	driver.get('https://finance.confused.com/?nt=1')
	ref=data['Reference'][i]
	btn1=driver.find_element_by_id('Purpose_'+str(ref)+'_Label').click()

	#---------------------------------------------
	amt=data['AmountBorrowed'][i]
	driver.find_element_by_id('LoanAmount').send_keys(int(amt))

	#----------------------------------
	select=Select(driver.find_element_by_id('Term'))
	trm=data['Term'][i]
	select.select_by_visible_text(str(trm))
	#-----------------------------------
	try:
		reg=data['CarReg'][i]
		driver.find_element_by_id('RegistrationNumber').send_keys(str(reg))
	except:
		print('reg no. not found')
	#------------------------------------------------------------

	time.sleep(2)
	try:
		c=driver.find_element_by_id('CookieConsentClose')
		if c:
			c.click()
	except:
		print("No cookie popup")
	driver.find_element_by_id('Car-Finance-Continue').click()

	time.sleep(1)

	#-----------------------------
	title=data['Title'][i]
	title_ids={"Mr":'2449','Mrs':'2451','Miss':'2450','Ms':'2452','Dr (Male)':'2453','Dr (Female)':'2454'}
	driver.find_element_by_id('Applicant_Title_'+title_ids[title]+'_Label').click()

	driver.find_element_by_id('Applicant_Firstname').send_keys(str(data['FirstName'][i]))
	driver.find_element_by_id('Applicant_Surname').send_keys(str(data['Surname'][i]))

	#-------------------------
	Select(driver.find_element_by_id('Applicant_DateOfBirth_Day')).select_by_value(str(data['DOB_Day'][i]))
	Select(driver.find_element_by_id('Applicant_DateOfBirth_Month')).select_by_visible_text(str(data['DOB_Month'][i]))
	Select(driver.find_element_by_id('Applicant_DateOfBirth_Year')).select_by_value(str(data['DOB_Year'][i]))

	#--------------------------------------------------
	status=str(data['Marrital_Status'][i])

	status_ids={"Married":'2457','Single':'2455','Living with partner/common law':'2456'}
	if status in status_ids.keys():
		driver.find_element_by_id('Applicant_MaritalStatus_'+status_ids[status]+'_Label').click()
	else:
		driver.find_element_by_id('Applicant_MaritalStatus_Applicant_MaritalStatus_More_Label').click()
		Select(driver.find_element_by_id('Select_Applicant_MaritalStatus')).select_by_visible_text(status)

	#---------------------------------
	child=str(data['Children'][i])

	if child=='Yes':
		driver.find_element_by_id('Applicant_ChildrenUnderSixteen_1_Label').click()
	else:
		driver.find_element_by_id('Applicant_ChildrenUnderSixteen_2_Label').click()
	#-----------------------------
	licen=str(data['Licence Type'][i])
	lics_ids={'Full UK-manual':'27777','Full Euro (EEC)':'27782'}
	if licen in lics_ids.keys():
		driver.find_element_by_id('Applicant_LicenceType_'+lics_ids[licen]+'_Label').click()
	else:
		driver.find_element_by_id('Applicant_LicenceType_Applicant_LicenceType_More_Label').click()
		Select(driver.find_element_by_id('Select_Applicant_LicenceType')).select_by_visible_text(licen)

	#------------------------------
	occ=str(data['Employment Status'][i])

	occ_ids={"Employed":'2435','Retired':'2437','Self-employed':'2436'}
	if occ in occ_ids.keys():
		driver.find_element_by_id('Applicant_EmploymentStatus_'+occ_ids[occ]+'_Label').click()
	else:
		driver.find_element_by_id('Applicant_EmploymentStatus_Applicant_EmploymentStatus_More_Label').click()
		Select(driver.find_element_by_id('Select_Applicant_EmploymentStatus')).select_by_visible_text(occ)

	try:
		f1=driver.find_element_by_id('Applicant_OccupationDetails_SearchText')
		f1.send_keys(data['Occupation Details'][i])
		time.sleep(3)
		f1.send_keys('\n')
		f2=driver.find_element_by_id('Applicant_IndustryDetails_SearchText')
		f2.send_keys(data['Industry'][i])
		time.sleep(3)
		f2.send_keys('\n')
		f3=driver.find_element_by_id('Applicant_EmployerName')
		f3.send_keys(data['Employer'][i])
	except:
		print('Some Data Missing/Incorrect')

	driver.find_element_by_id('About-You-Continue').click()
	time.sleep(1)
	#---------------------------------

	driver.find_element_by_id('Applicant_EmailAddress').send_keys(str(data['Email'][i]))
	driver.find_element_by_id('Applicant_PhoneNumber').send_keys("0"+str(data['Phone Number'][i]))

	#--
	own=data['Home Owner'][i]
	if own=='Yes':
		driver.find_element_by_id('Applicant_IsHomeOwner_1_Label').click()
	else:
		driver.find_element_by_id('Applicant_IsHomeOwner_2_Label').click()
	#--

	driver.find_element_by_id('Applicant_Postcode').send_keys(str(data['Post Code'][i]))
	driver.find_element_by_id('findaddress').click()
	time.sleep(2)
	Select(driver.find_element_by_id('Applicant_DateMovedIn_Month')).select_by_visible_text(str(data['Move In Date'][i]))
	Select(driver.find_element_by_id('Applicant_DateMovedIn_Year')).select_by_visible_text(str(data['Move In Year'][i]))
	driver.find_element_by_id('add-address').click()
	time.sleep(1)
	driver.find_element_by_id('Contact-Details-Continue').click()
	#------------

	driver.find_element_by_id('Applicant_AnnualIncome').send_keys(str(data['Annual Income'][i]))
	driver.find_element_by_id('Applicant_MonthlyMortgageOrRentPayments').send_keys(str(data['Payments'][i]))
	driver.find_element_by_id('Applicant_OtherMonthlyOutgoings').send_keys(str(data['Other outgoings'][i]))

	#-----------------
	driver.find_element_by_id('IsOptedIn').click()
	driver.find_element_by_id('IsTermsConditionsAccepted').click()
