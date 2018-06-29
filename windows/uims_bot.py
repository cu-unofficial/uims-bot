import mechanize
from bs4 import BeautifulSoup
import requests
import telepot
import time
import io


TOKEN = ''
CHANNEL = ''

USER_ID = ''
USER_PASS = ''

URL = 'https://uims.cuchd.in/UIMS/StaffHome.aspx/DisplayAnnouncements'
DATA = "{Category:'ALL', PageNumber:'1', FilterText:''}"


def ready_browser():
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_handle_redirect(True)
    browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
    return browser


def request_headers(session_id):
    headers = { 'Content-Type': 'application/json; '
                                'charset=utf-8',
                'Cookie': 'UIMSLoginCookie9/23/2017=5UEoMJNbNYoKyTkYkVG+kg==; '
                          'ASP.NET_SessionId={}; '
                          'StudentMyMessagesCookie=00XXX0000' }
    headers['Cookie'] = headers['Cookie'].format(session_id)
    return headers


def cuims_session(browser):
    browser.open('https://uims.cuchd.in/uims/')
    browser.select_form(nr=0)
    browser['txtUserId'] = USER_ID
    browser.submit()

    browser.select_form(nr=0)
    browser['txtLoginPassword'] = USER_PASS
    browser.submit()

    session_id = browser.cookiejar[0].value
    browser.close()
    return session_id


def parasable_form(html):
    html = html.replace('\\', '')
    html = html.replace('u003c', '<')
    html = html.replace('u003e', '>')
    html = html.replace('u0026nbsp;', ' ')
    html = html.replace('u0026amp;', '&')
    html = html.replace('u0026middot;', '-')
    html = html.replace('u0027', "'")
    html = html.replace('u0026', '&')
    html = html.replace('<br/>', '\n')
    return html


def extract_message(message, headers):
    msg_title = message.find('h3').get_text()
    msg_date = message.find('span', {'class':'post-dd-tt'}).get_text().strip()
    msg_body = message.find('p').get_text().strip()
    msg_uploader = message.find('span', {'class':'uploded-user'}).get_text()

    try:
        msg_image = []
        images = message.find('p').find_all('img')
        for image in images:
            b64_data = image['src'].split(',')[1]
            b64_decoded = b64_data.decode('base64')
            memory_image = io.BytesIO(b64_decoded)
            msg_image.append(memory_image)
    except:
        pass

    try:
        msg_attachment = []
        attachment_names = message.find_all('div', {'class':'aQA'})
        attachments = message.find_all('vijay', {'class':'download_button'})
        for n, attachment in enumerate(attachments):
            attachment_name = attachment_names[n].find('span').get_text().replace(' ', '_')
            attachment_link = attachment.find('a')['href']
            absolute_link = 'https://uims.cuchd.in/UIMS/' + attachment_link[3:]
            response = requests.get(absolute_link, headers=headers)
            memory_attachment = io.BytesIO(response.content)
            msg_attachment.append((attachment_name, memory_attachment))
    except:
        pass

    msg_dict = { 'title'      : msg_title,
                 'date'       : msg_date,
                 'body'       : msg_body,
                 'uploader'   : msg_uploader,
                 'image'      : msg_image,
                 'attachment' : msg_attachment }

    return msg_dict


def compile_message(msg):
    c_msg = msg['title']
    c_msg += '\n\n[' + msg['date'] + ']'
    c_msg += '\n\n' + msg['body']
    c_msg += '\n\n' + msg['uploader']
    return c_msg


def update_headers():
    browser = ready_browser()
    session_id = cuims_session(browser)
    headers = request_headers(session_id)
    return headers


bot = telepot.Bot(TOKEN)
old_date = ''
print('initializing headers')

while True:
    try:
        headers = update_headers()
        break
    except KeyboardInterrupt:
        headers = ''
        break
    except:
        pass


while True:
    try:
        print('requesting data')
        response = requests.post(URL,
                             headers=headers,
                             data=DATA,
                             timeout=600)
        status_code = response.status_code

        if not status_code == 200:
            print('return code: {}, refreshing headers'.format(status_code))
            headers = update_headers()
            continue

        parsable_html = parasable_form(response.text)
        soup = BeautifulSoup(parsable_html, 'html.parser')

        messages = soup.find_all('div', {'class':'postsection-wrap'})
        message = extract_message(messages[0], headers)
        send_message = not (message['date'] == old_date or old_date == '')

        if send_message:
            tg_message = compile_message(message)
            print(tg_message)
            bot.sendMessage(CHANNEL, tg_message)

            for image in message['image']:
                bot.sendPhoto(CHANNEL, image, disable_notification=True)
            for attachment in message['attachment']:
                bot.sendDocument(CHANNEL, attachment, disable_notification=True)

        old_date = message['date']
        time.sleep(120)


    except KeyboardInterrupt:
        break

    except Exception as e:
        print(e)
