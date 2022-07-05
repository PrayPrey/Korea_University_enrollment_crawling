# Korea_University_enrollment_crawling
고려대학교 수강신청 사이트를 크롤링한 코드입니다. (2020년 이후 사이트)

- Scrapy와 Selenium을 혼용하여 사용하였습니다.
- 지번 추가는 카카오 API에 연결하여 추가하였습니다. (본인의 KAKAO API AUTHORIZATION을 입력하시면 됩니다)
- Scarpy 작동 시에 Selenium이 같이 돌아가도록 만들었으며, Chromedriver는 같은 경로상에 위치하여야 합니다.
- Scrapy 사용법과 Selenium 사용법은 공식 홈페이지를 참조하시면 됩니다.
- 혹시 사용하다가 불편하신 부분이 있다면 Issues에 남기면 연락드리겠습니다. 제가 사정이 되는 한 알려드리겠습니다.



# 2022_07_06 변경
- 2022_고려대학교_Data_campus 수업을 듣고 변경한 코드입니다 (sugang_new.ipynb)
- selenium, scrapy 사용없이 전공, 교양, 교직 과목을 1분안에 모두 크롤링할 수 있습니다.
- 마지막 df3 부분의 column을 고치면, 더 많은 정보를 볼 수 있습니다
- 예시 크롤링한 파일은 1.csv 파일입니다.
