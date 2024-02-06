import bs4
from bs4 import Comment
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# Language(s) (NLP): English, Portuguese, Spanish, French, German, Dutch, Italian, Korean, Chinese, Russian


class WebpageTranslator:
    def __init__(self, input_language, output_language):
        self.lang_code = {
            'english': 'en_XX',
            'german': 'de_DE',
            'french': 'fr_XX',
            'chinese': 'zh_CN',
            'portuguese': 'pt_XX',
            'dutch': 'nl_XX',
            'russian': 'ru_RU',
            'korean': 'ko_KR',
            'italian': 'it_IT',
            'spanish': 'es_XX'
        } 
        self.inp_lang = input_language
        self.outp_lang = output_language

    def TowerBase_get_lanuage(self, language):
        self.towerbase_inp_lang = language
        code = self.lang_code[language.lower()]
        if code:
            return code.split('_')[0]
        else: 
            print('[+] Output language not in our Library...')

    def MBart_get_language(self, language):
        code = self.lang_code[language.lower()]
        if code:
            return code
        else: 
            print('[+] Output language not in our Library...')

    @staticmethod
    def TowerBase_load_model():
        tokenizer = AutoTokenizer.from_pretrained('Unbabel/TowerBase-7B-v0.1')
        model = AutoModelForCausalLM.from_pretrained('Unbabel/TowerBase-7B-v0.1')
        print('[+] Model loaded successfully')
        return model, tokenizer

    @staticmethod
    def MBart_load_model():
        model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        print('[+] Model loaded successfully')
        return model, tokenizer

    def TowerBase_translate(self, sentence, model, tokenizer):
        if model and tokenizer and isinstance(sentence, str):
            prefix = self.inp_lang.captalize() + ': '
            suffix = '\n'+ self.outp_lang.captalize() + ':'
            sentence = prefix + sentence + suffix
            inputs = tokenizer(sentence, return_tensors="pt")
            outputs = model.generate(**inputs, max_new_tokens=20)
            sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
            sentence = sentence.split('Portuguese:')[1].strip()
        return sentence

    @staticmethod
    def MBart_translate(sentence, model, tokenizer, code):
        if model and tokenizer and isinstance(sentence, str):
            print(sentence)
            encoded_hi = tokenizer(sentence, return_tensors='pt')
            generated_tokens = model.generate(**encoded_hi, forced_bos_token_id=tokenizer.lang_code_to_id[code])
            sentence = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return sentence

    def translate_method(self, sentence, model, tokenizer, translator, code):
        if translator == 'MBart':
            result = self.MBart_translate(sentence, model, tokenizer, code)
            return result
        elif translator == 'TowerBase':
            result = self.TowerBase_translate(sentence, model, tokenizer)
            return result

    @staticmethod
    def remove_spaces(sentence):
        words = sentence.split(' ')
        return ' '.join([x for x in words if x])


    def translate(self, tag, model, tokenizer, translator, code):
        if isinstance(tag, bs4.element.Tag):
            if tag.name not in ['script']:
                for i in range(len(tag.contents)):
                    if isinstance(tag.contents[i], bs4.element.Tag):
                        if 'alt' in tag.contents[i].attrs:
                            text = self.remove_spaces(tag.contents[i].attrs['alt'].strip())
                            tag.contents[i].attrs['alt'] = self.translate_method(text, model, tokenizer, translator, code)
                        self.translate(tag=tag.contents[i], model=model, tokenizer=tokenizer, translator=translator, code=code)
                    else:                
                        if tag.contents[i].strip() not in ['\n', '']:
                            if not isinstance(tag.contents[i], Comment):
                                text = self.remove_spaces(tag.contents[i].strip())
                                tag.contents[i].replace_with(self.translate_method(text, model, tokenizer, translator, code))

    @staticmethod
    def save_file(soup, file_path):
        # save file to html
        print(file_path)
        soup_output = soup.prettify('utf-8')
        with open(file_path, "wb") as file:
            file.write(soup_output)
        file.close()
