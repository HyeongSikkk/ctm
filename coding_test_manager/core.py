import requests
from bs4 import BeautifulSoup as BS
import subprocess

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
        
    def get_page(self):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        r = requests.get(self.url, headers = header)
        self.page = BS(r.text, 'html.parser')
        
    def find_test_case(self):
        test_cases = []
        cnt = 0
        while True :
            cnt += 1
            target_input = f"sampleinput{cnt}"
            target_output = f"sampleoutput{cnt}"
            try :
                test_case_input = self.page.find(id = target_input).find('pre').text
                test_case_output = self.page.find(id = target_output).find('pre').text
                test_case = {
                    'test_case_input' : test_case_input,
                    'test_case_output' : test_case_output,
                          }
                test_cases.append(test_case)
            except :
                break
        self.test_cases = test_cases
        
    def do_test(self, file_path) :
        '''
        백준에서 주어지는 샘플 데이터로 테스트 하는 메서드입니다.
        작성하신 코드를 파이썬 파일로 저장하고, 해당 파일의 경로를 file_path 변수로 전달해주세요.
        '''
        cmd = f"python {file_path}"
        for test_case in self.test_cases :
            sample_input, sample_output = test_case.values()
            result = subprocess.run(cmd, input = sample_input, text = True, capture_output=True)
            print(f"기댓값\n{sample_output.strip()}\n결과괎\n{result.stdout.strip()}\n{'성공' if sample_output.strip() == result.stdout.strip() else '실패'}")
        