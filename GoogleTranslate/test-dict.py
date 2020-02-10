# File Name : test-dict
# @date : 2020-02-07  20:12
'''
Language = {
            "Auto": "auto",
            "English": "en",
            "Chinese": "zh-CN",
            "German": "de",
            "Russian": "ru",
            "Japanese": "ja",
            "French": 'fr',
            "Korea": "ko",
        }

print(Language.keys())
S = "Ato"
if S in Language.keys():
    print(Language[S])


for i,j in Language.items():
    print(i)

# ii = "Auto"/"English"/"Chinese"/"German"/"Russian"/"Japanese"/"French"/"Korea"
'''

def switch(language='Auto'):
    Language = {
        "Auto": "auto",
        "English": "en",
        "Chinese": "zh-CN",
        "German": "de",
        "Russian": "ru",
        "Japanese": "ja",
        "French": 'fr',
        "Korea": "ko",
    }
    if language in Language.keys():
        return Language[language]
print(switch())