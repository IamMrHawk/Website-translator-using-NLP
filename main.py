from translator import WebpageTranslator
import os
from glob import glob
from bs4 import BeautifulSoup
import requests


class TranslateWebpages:
        def __init__(
                self, 
                translator, 
                language, 
                output_dir, 
                model_name, 
                input_language,dir_path=None,
                url_file=None, 
                get_dir=False, 
                get_url=False
        ):
                
                self.translator = translator
                self.language = language
                self.output_dir = output_dir
                self.dir_path = dir_path
                self.url_file = url_file
                self.get_dir = get_dir
                self.get_url = get_url
                self.model_name = model_name
                self.input_language = input_language

                # get translation code to translate
                # code = WebpageTranslator.TowerBase_get_lanuage(language=language)
                
                
                # load models
                        ## MBart -> less accurate, requires small gpu or 4gb RAM, No cost required
                        ## TowerBase -> more accurate, requires >16GB GPU or >16GB RAM, No cost required
                        ## CHATGPT -> most accurate, No GPU required, Cost you according to your API plan

                if self.model_name == 'MBart':
                        self.code = self.translator.MBart_get_language(language=self.language)
                        self.inputlang_code = self.translator.MBart_get_language(language=self.input_language)
                        ## loading MBart
                        self.model, self.tokenizer = self.translator.MBart_load_model()
                        self.tokenizer.src_lang = self.inputlang_code
                elif self.model_name == 'TowerBase':
                        ## loading TowerBase
                        model, tokenizer = WebpageTranslator.TowerBase_load_model()
                else:
                        print("[-] Please mention model_name from ['MBart', 'TowerBase']")
                        exit(1)
                

                if self.get_dir != None:
                        # list of all html files to translate
                        self.all_files = glob(os.path.join(self.dir_path, "**/*.html"), recursive=True)
                        self.TranslateFiles()

                elif get_url != None:
                        # get all urls
                        file = open(self.url_file, 'r')
                        self.all_urls = file.read()
                        self.all_urls = self.all_files.split('\n')
                        self.TranslateUrls()

                else:
                        print('[-] Please mention Either Urls or HTML files directory path')
                        exit(1)


        def TranslateFiles(self):
                for html_file in self.all_files:
                        file = open(html_file, 'r', encoding="utf8")
                        html_text = file.read()
                        file.close()

                        soup = BeautifulSoup(html_text, 'lxml')
                        html = soup.find('body')
                        # translator -> MBart or TowerBase
                        self.translator.translate(tag=html, model=self.model, tokenizer=self.tokenizer, translator='MBart', code=self.code)

                        path = os.path.join(self.output_folder, html_file.split('\\')[-1])
                        self.translator.save_file(soup=soup, file_path=path)
                        print(f'[+] Translation complete : {html_file}')

        def TranslateUrls(self):
                session = requests.session()
                for url in self.all_urls:
                        response = session.get(url)
                        soup = BeautifulSoup(response.content, 'lxml')
                        html = soup.find('body')
                        file_name = soup.find('title').text
                        # translator -> MBart or TowerBase
                        self.translator.translate(tag=html, model=self.model, tokenizer=self.tokenizer, translator='MBart', code=self.code)

                        path = os.path.join(self.output_folder, file_name)
                        self.translator.save_file(soup=soup, file_path=path)
                        print(f'[+] Translation complete : {url}')

        


if __name__ == '__main__':
        
        # get translation language code
        # Input/Output Languages : English, Portuguese, Spanish, French, German, Dutch, Italian, Korean, Chinese, Russian
        language = 'spanish'
        input_language = 'English'
        output_dir = 'C:\Users\UE\Documents\Python Scripts\output'
        model_name = 'MBart' # or 'TowerBase'        

        translator = WebpageTranslator(input_language=input_language, output_language=language)

        main = TranslateWebpages(
                translator=translator,
                language=language,
                output_dir=output_dir,
                model_name=model_name,
                input_language=input_language
        )
        
