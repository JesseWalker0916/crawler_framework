import base64
import datetime
import email
import json
import os.path
import time
import undetected_chromedriver as uc
from typing import Optional, List
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from config import Config

# 自动生成下载目录
pdir = Config.get_url()


def ck_dir(*args, file: bool = False, ) -> str:
    if len(args) == 1:
        path = args[0]
    else:
        path = os.path.join(*args)

    c_path = path
    try:
        if file or "." in os.path.split(path)[1]:
            c_path = os.path.split(path)[0]
    except:
        pass

    if os.path.exists(c_path):
        return path

    os.makedirs(c_path)
    return path


class Driver:
    type_dict = {"class": By.CLASS_NAME, "id": By.ID, "xpath": By.XPATH, "name": By.NAME}
    d: uc.Chrome = None

    # windows驱动
    def windows_driver(self, c_sel_path: str = None):
        if not c_sel_path:
            c_sel_path = os.path.join(pdir, "public", "chromedriver.exe")

        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')  # selenium禁用gpu
        options.add_argument('--enable-print-browser')  # selenium禁用gpu
        options.add_argument('--no-sandbox')  # selenium不在root用户下执行
        options.add_argument('--disable-blink-features')
        options.add_argument('--kiosk-printing')  # 静默打印
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--lang=zh-CN,zh,zh-TW,en-US,en')
        options.add_argument('--save-page-as-mhtml')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
            "isHeaderFooterEnabled": False,
            "isCssBackgroundEnabled": True,
            "mediaSize": {
                "height_microns": 297000,
                "name": "ISO_A4",
                "width_microns": 210000,
                "custom_display_name": "A4"
            },
        }

        # 指定下载路径
        cur_path = ck_dir(pdir, "downloads")
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'download.default_directory': cur_path,
            'savefile.default_directory': cur_path,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        options.add_experimental_option('prefs', prefs)

        _desired_capabilities = DesiredCapabilities.CHROME
        _desired_capabilities["pageLoadStrategy"] = "none"

        # 执行selenium的driver
        self.d = uc.Chrome(
            options=options, desired_capabilities=_desired_capabilities, driver_executable_path=c_sel_path)
        # self.d = webdriver.Chrome(service=Service(executable_path=c_sel_path, options=options))

    # 获取驱动
    def get_driver(self, sys: str):

        if sys.lower() == "windows":
            self.windows_driver()
            self.d.maximize_window()

        # 设置大小
        self.d.set_window_size(1920, 1080, windowHandle="current")
        if sys.lower() == "windows":
            self.d.maximize_window()
        return self.d

    # 关闭驱动
    def close(self):
        if self.d:
            self.d.close()
            self.d.quit()
            del self.d
            self.d = None

    # 获取页面元素
    def get_element(self, el_type, element, err=False, err_msg="", t=1) -> WebElement:
        cur_type = self.type_dict.get(el_type)
        try:
            if type(element) == str:
                self.d.implicitly_wait(t)
                result = self.d.find_element(cur_type, element)
                result.element = element  # 返回结果添加命中选项
                return result
            elif type(element) == list:
                self.d.implicitly_wait(t)
                for i in element:
                    try:
                        result = self.d.find_element(cur_type, i)
                        result.element = i  # 返回结果添加命中选项
                        return result
                    except Exception as e:
                        self.d.implicitly_wait(1)
                else:
                    raise e
        except:
            if err:
                if err_msg:
                    raise Exception(err_msg)
                else:
                    raise Exception("HTML_ERROR***element not found!!!")

            return None

    # 获取页面元素列表
    def get_elements(self, el_type, element, err=False, t=1) -> Optional[List[WebElement]]:
        cur_type = self.type_dict.get(el_type)
        self.d.implicitly_wait(t)
        result = []
        if cur_type is None:
            return []

        for _ in range(t):
            try:
                if isinstance(element, str):
                    return self.d.find_elements(cur_type, element)
                elif isinstance(element, list):
                    for i in element:
                        result.extend(self.d.find_elements(cur_type, i))
            except:
                time.sleep(1)
        else:
            if not result and err:
                raise Exception("HTML_ERROR***element not found!!!")

            return result

    def el_get_element(self, el_obj: WebElement, el_type, element, err_msg="", err=False, t=1) -> WebElement:
        cur_type = self.type_dict.get(el_type)

        for _ in range(t):
            try:
                if type(element) == str:
                    result = el_obj.find_element(cur_type, element)
                    result.element = element  # 返回结果添加命中选项
                    return result
                elif type(element) == list:
                    for i in element:
                        try:
                            result = el_obj.find_element(cur_type, i)
                            result.element = i  # 返回结果添加命中选项
                            return result
                        except:
                            pass
            except:
                time.sleep(1)
        else:
            if err:
                if err_msg:
                    raise Exception(err_msg)
                else:
                    raise Exception("HTML_ERROR***element not found!!!")

            return None

    # 获取页面元素列表
    def el_get_elements(self, el_obj: WebElement, el_type, element, err=False, t=1) -> Optional[List[WebElement]]:
        cur_type = self.type_dict.get(el_type)
        if cur_type is None:
            return []

        for _ in range(t):
            try:
                if type(element) == str:
                    return el_obj.find_elements(cur_type, element)
                elif type(element) == list:
                    for i in element:
                        try:
                            return el_obj.find_elements(cur_type, i)
                        except:
                            pass
            except:
                time.sleep(1)
        else:
            if err:
                raise Exception("HTML_ERROR***element not found!!!")
            return []

    # 向元素输入值
    def send_element(self, el_type, element, text, err_msg="", t=1):
        cur_type = self.type_dict.get(el_type)
        self.d.implicitly_wait(t)
        try:
            return self.d.find_element(cur_type, element).send_keys(text)
        except Exception:
            if err_msg:
                raise Exception(err_msg)
            else:
                return Exception("HTML_TIMEOUT***get element timeout!!!!!")

    # 删除元素
    def del_element(self, el_type, elements: list, el: WebElement = None):
        for el_str in elements:
            if el:
                f_els = self.el_get_elements(el, el_type, el_str, t=1)
            else:
                f_els = self.get_elements(el_type, el_str, t=1)

            for el_obj in f_els:
                self.d.execute_script("arguments[0].style.display='none'", el_obj)

    # 检测页面标题
    def check_title(self, title, t=10):
        for _ in range(t):
            try:
                WebDriverWait(self.d, 1).until(EC.title_is(u"%s" % title))
                return True
            except Exception:
                time.sleep(1)
        else:
            raise Exception("PATH_ERROR***check title timeout!!!")

    # 截图
    def screen_shot(self, level: str, date=True):
        cur_path = ck_dir(pdir, "shot")

        # 拼接存储类型
        cur_path = ck_dir(cur_path, level)
        ck_dir(cur_path)

        now = int(time.time())
        # 是否区分日期目录
        if date:
            datetime_now = datetime.datetime.now()
            # 年份
            year = str(datetime_now.year)
            # 月份
            month = str(datetime_now.month).zfill(2)
            # 日期
            day = str(datetime_now.day).zfill(2)

            # 检查目录
            cur_path = ck_dir(cur_path, year, month, day)

        # 截图
        file_name = f"{level}_{now}.png"
        file_path = ck_dir(cur_path, file_name)
        self.d.get_screenshot_as_file(file_path)

        return file_path

    def send(self, cmd, params=None):
        if params is None:
            params = {}
        resource = "/session/%s/chromium/send_command_and_get_result" % self.d.session_id
        url = self.d.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = self.d.command_executor._request('POST', url, body)
        return response.get('value')

    # 保存为mhtml
    def save_mhtml_file(self, save_path: str):
        res = self.send('Page.captureSnapshot', {})
        ck_dir(os.path.split(save_path)[0])
        with open(save_path, 'w+', newline='') as sf:
            sf.write(res['data'])
        return save_path

    def get_mhtml(self) -> str:
        res = self.send('Page.captureSnapshot', {})
        return res["data"]

    def get_css_img(self) -> (list, dict, dict):
        css_lis = []
        img_dic = {}
        sav_bs = {}
        for part in email.message_from_string(self.get_mhtml()).walk():
            if part.get("Content-Type") == "text/css":
                css_str = part.get_payload(decode=True).decode().replace('@charset "utf-8";\n', "")
                css_lis.append(css_str)

            elif "image" in part.get("Content-Type"):
                img_dic[part.get("Content-Location")] = part.get_payload().strip()

                sav_bs[part.get(
                    "Content-Location")] = f'data:{part.get("Content-Type")};base64,{part.get_payload().strip()}'

        return css_lis, img_dic, sav_bs

    def save_pdf(self, save_path: str):
        pdf_name = os.path.split(save_path)[1]
        resource = "/session/%s/chromium/send_command_and_get_result" % self.d.session_id
        url = self.d.command_executor._url + resource
        body = json.dumps({'cmd': "Page.printToPDF", 'params': {}})
        response = self.d.command_executor._request('POST', url, body)
        cur_path = ck_dir(pdir, "downloads")
        with open(os.path.join(cur_path, pdf_name), "wb") as fp:
            fp.write(base64.b64decode(response.get('value')["data"]))
        return pdf_name

    def get_el_html(self, element: WebElement):
        return self.d.execute_script("""
            var element = arguments[0];
            var computedStyle = window.getComputedStyle(element, null);
            var cssText = "";
            for (var i = 0; i < computedStyle.length; i++) {
                var property = computedStyle[i];
                var value = computedStyle.getPropertyValue(property);

                var defaultStyle = window.getComputedStyle(document.createElement(element.tagName), null);
                var defaultValue = defaultStyle.getPropertyValue(property);

                // 过滤掉默认设置的样式
                if (!(value === defaultValue)) {
                    cssText += property + ": " + value + ";\\n";
                }
            }
            element.setAttribute('style', cssText);

            var children = element.children;
            for (var i = 0; i < children.length; i++) {
                arguments.callee(children[i]);
            }

            return element.outerHTML;
        """, element)
