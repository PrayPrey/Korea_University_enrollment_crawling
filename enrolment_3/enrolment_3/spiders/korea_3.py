import scrapy
from enrolment_3.items import Enrolment3Item

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from scrapy.selector import Selector

class Korea3Spider(scrapy.Spider):
    name = 'korea_3'

    def start_requests(self):
        chromedriver = 'chromedriver.exe'
        driver = webdriver.Chrome(chromedriver)
        driver.get('http://sugang.korea.ac.kr')       
        yield scrapy.Request(url = 'http://sugang.korea.ac.kr',callback = self.parse_category)

    def __init__(self):
        # 기존 Spider 클래스의 생성자를 call해서 초기화해준다.
        scrapy.Spider.__init__(self)


        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("lang=ko_KR")
        options.add_argument("User-Agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Chrome/65.0")
        self.driver = webdriver.Chrome(options = options)

    def parse_category(self, response):
        self.driver.get(response.url)
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        time.sleep(3)
        element_1 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.jconfirm-closeIcon')))
        element_1.click()

        element_2 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.wrap-schedule span#menu_hakbu')))
        element_2.click()

        self.driver.switch_to.frame('coreMain')
        time.sleep(2)
        select_0 = Select(self.driver.find_element_by_css_selector('#pTerm'))
        select_0.select_by_visible_text('1학기')
        time.sleep(0.5)

        select = Select(self.driver.find_element_by_css_selector("#pCourDiv"))# (전공,교양)  selector 
        select_2 = Select(self.driver.find_element_by_xpath('//*[@id="pCol"]')) # 대학 selector
        
        segment = self.driver.find_elements_by_css_selector('#pCourDiv > option') #  (전공,교양)  data 
        segment_2 = self.driver.find_elements_by_xpath('//*[@id="pCol"]/option') # 대학  데이터

        # see = self.driver.find_element_by_css_selector('#btnSearch')

        # see.click()
        list_all = []

        for j in segment_2:
            
            select_2.select_by_visible_text(j.text)
            select_4 = Select(self.driver.find_element_by_css_selector('#pDept')) # 학과 selector
            segment_4 = self.driver.find_elements_by_xpath('//*[@id="pDept"]/option') # 학과 데이터
            
            for k in segment_4:          
                list_all.append([j.text,k.text])


        list_all_2 = []
        select.select_by_visible_text('교양')
        time.sleep(1)
        select_3 = Select(self.driver.find_element_by_css_selector('#pGroupCd')) # 교양  selector
        segment_3 = self.driver.find_elements_by_css_selector('#pGroupCd > option') # 교양  데이터
        for k in segment_3:
            select_3.select_by_visible_text(k.text)
            list_all_2.append(k.text)
        print(len(list_all),len(list_all_2))

        count = 0
        for i in list_all:
            yield scrapy.Request(url = 'http://sugang.korea.ac.kr',callback = self.end_point, meta = {'college':i[0],'major':i[1],'count':count})
            count += 1
        count = 0
        for j in list_all_2:
            yield scrapy.Request(url = 'http://sugang.korea.ac.kr',callback = self.end_point_2, meta = {'liberal':j,'count':count})
            count += 1




    def end_point_2(self,response):

        self.driver.get(response.url)



        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        # self.driver.switch_to.frame(iframe)
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"Main")))
        time.sleep(1.5)
        element_1 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.jconfirm-closeIcon'))).click()
        element_2 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div.wrap-schedule span#menu_hakbu'))).click()
        time.sleep(2)



        
        # self.driver.switch_to.frame('coreMain')
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"coreMain")))
        select_0 = Select(self.driver.find_element_by_css_selector('#pTerm'))
        select_0.select_by_visible_text('1학기')
        time.sleep(1)

 
        select = Select(self.driver.find_element_by_css_selector("#pCourDiv"))# (전공,교양)  selector 
        select.select_by_visible_text('교양')
        time.sleep(1)

        select_2 = Select(self.driver.find_element_by_xpath('//*[@id="pCol"]')) # 대학 selector
        select_3 = Select(self.driver.find_element_by_css_selector('#pGroupCd')) # 교양  selector
        segment = self.driver.find_elements_by_css_selector('#pCourDiv > option') #  (전공,교양)  data 
        segment_2 = self.driver.find_elements_by_xpath('//*[@id="pCol"]/option') # 대학  데이터
        segment_3 = self.driver.find_elements_by_name('pGroupCd') # 교양  데이터
        see = self.driver.find_element_by_xpath('//*[@id="btnSearch"]') 




        select_3.select_by_visible_text(response.meta['liberal'])

        time.sleep(1)
        see = self.driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
        time.sleep(2)

        html = self.driver.page_source

        selector = Selector(text = html) 

        table = selector.css('div.contents div.dataTables_scrollBody table#gridLecture tbody')
        count = 1
        print(response.meta['liberal'],response.meta['count'])
        for row in table.css('tr'): 

            doc = Enrolment3Item()
            if '검색결과가 존재하지 않습니다. None 조회 조건 선택 후 조회 버튼을 클릭하세요.' in row.css('td::text').getall():
                pass
            doc['entire'] = response.meta['liberal']
            doc['campus'] = row.css('td.dt-body-center::text')[0].get()
            doc['number'] = row.css('td span::text')[0].get()
            doc['class_'] =  row.css('td.dt-body-center::text')[1].get()
            doc['seperate'] =   row.css('td.dt-body-center::text')[2].get()
            doc['major'] =  row.css('td.dt-body-center::text')[3].get()
            try:
                doc['class_name'] = row.xpath('./td[6]/span/text()').get()+' '+row.xpath('./td[6]/text()').get()

            except:
                doc['class_name'] = row.xpath('./td[6]/span/text()').get()
            doc['prof'] =  row.css('td.dt-body-center::text')[4].get().replace('\n','').replace(',',' ')
            doc['time'] =  row.css('td.dt-body-center::text')[5].get()
            
            try:
                doc['place'] = row.xpath('./td[9]/text()[1]').get().replace('\n','').replace(',',' ') +' '+ row.xpath('./td[9]/text()[2]').get().replace('\n','').replace(',',' ').strip()
            except:
                doc['place'] = row.xpath('./td[9]/text()').get()

            yield doc






    def end_point(self,response):

        self.driver.get(response.url)



        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        # self.driver.switch_to.frame(iframe)
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"Main")))
        time.sleep(1.5)
        element_1 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.jconfirm-closeIcon'))).click()
        element_2 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div.wrap-schedule span#menu_hakbu'))).click()
        time.sleep(2)



        # self.driver.switch_to.frame('coreMain')
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"coreMain")))

        select_0 = Select(self.driver.find_element_by_css_selector('#pTerm'))
        select_0.select_by_visible_text('1학기')



        select = Select(self.driver.find_element_by_css_selector("#pCourDiv"))# (전공,교양)  selector 
        select.select_by_visible_text('전공')




        select_2 = Select(self.driver.find_element_by_xpath('//*[@id="pCol"]')) # 대학 selector
        segment_2 = self.driver.find_elements_by_xpath('//*[@id="pCol"]/option') # 대학  데이터        
        segment_4 = self.driver.find_elements_by_css_selector('#pDept > option') # 학과 데이터
        select_4 = Select(self.driver.find_element_by_xpath('//*[@id="pDept"]')) 
        

        select_2.select_by_visible_text(response.meta['college'])
        time.sleep(1)
        select_4.select_by_visible_text(response.meta['major'])
        see = self.driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
        time.sleep(2)
        print(response.meta['college'],response.meta['major'],response.meta['count'])

        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,'div.contents div.dataTables_scrollBody table#gridLecture tbody tr')))
        html = self.driver.page_source
        selector = Selector(text = html) 

        table = selector.css('div.contents div.dataTables_scrollBody table#gridLecture tbody')
        for row in table.css('tr[role="row"]'):           
            doc = Enrolment3Item()
            if '검색결과가 존재하지 않습니다. None 조회 조건 선택 후 조회 버튼을 클릭하세요.' in row.css('td::text').getall():
                pass
            doc['entire'] = response.meta['college']
            doc['campus'] = row.css('td.dt-body-center::text')[0].get()
            doc['number'] = row.css('td span::text')[0].get()
            doc['class_'] =  row.css('td.dt-body-center::text')[1].get()
            doc['seperate'] =   row.css('td.dt-body-center::text')[2].get()
            doc['major'] =  row.css('td.dt-body-center::text')[3].get()
            try:
                doc['class_name'] = row.xpath('./td[6]/span/text()').get()+' '+row.xpath('./td[6]/text()').get()

            except:
                doc['class_name'] = row.xpath('./td[6]/span/text()').get()
            doc['prof'] =  row.css('td.dt-body-center::text')[4].get().replace('\n','').replace(',',' ')
            doc['time'] =  row.css('td.dt-body-center::text')[5].get()
            
            try:
                doc['place'] = row.xpath('./td[9]/text()[1]').get().replace('\n','').replace(',',' ').strip() +' '+ row.xpath('./td[9]/text()[2]').get().replace('\n','').replace(',',' ')
            except:
                doc['place'] = row.xpath('./td[9]/text()').get()

            yield doc







