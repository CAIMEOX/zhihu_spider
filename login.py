from DecryptLogin import login
import cookielib
def login_zhihu():
    lg = login.Login()
    info, session = lg.zhihu()
    print(info, session)
    for cookie in session.cookies:
        print(cookie)  
    return 

login_zhihu()
