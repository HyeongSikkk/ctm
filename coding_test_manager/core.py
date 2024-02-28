import requests
from bs4 import BeautifulSoup as BS

def manager(url) :
    if 'programmers' in url :
        return Programmers(url)
    elif 'acmicpc' in url :
        return Acmicpc(url)
        
class Manager :
    def __init__(self, url) :
        self.url = url
        self.get_page()
        self.find_test_case()
        
    def get_page(self) :
        raise NotImplementedError()
    
    def find_test_case(self) :
        raise NotImplementedError()
    
    def do_test(self, func) :
        raise NotImplementedError()
            

class Programmers(Manager) :
    def __init__(self, url) :
        super().__init__(url)
        
    def get_page(self) :
        r = requests.get(self.url)
        if r.status_code != 200 :
            raise f"문제 url이 유효하지 않습니다. requests code {r.status_code}"
        bs = BS(r.text, features="html.parser")
        self.page = bs.find('div', {'class' : 'guide-section-description'})
    
    def find_test_case(self) :
        test_cases = []
        keys = []
        for idx, row in enumerate(self.page.find('table').findAll('tr')) :
            if idx == 0 :
                keys = row.findAll('th')
                keys = list(map(lambda x : x.text, keys)) # [<th>result</th>] -> ['result']
            else :
                test_case = {}
                for key, value in zip(keys, row.findAll('td')) :
                    test_case[key] = value.text
                test_cases.append(test_case)
        self.test_cases = test_cases
    
    def do_test(self, func) :
        result_text = "기댓값 {}, 결과값 {}, {}"
        for test_case in self.test_cases :
            rows = test_case.values()
            rows = list(map(eval, rows))
            test_result = func(*rows[:-1])
            print(result_text.format(rows[-1], test_result, '성공' if test_result == rows[-1] else '실패'))
            

class Acmicpc(Manager) :
    def __init__(self, url) :
        super().__init__(url)