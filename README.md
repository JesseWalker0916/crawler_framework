# 开箱即用的爬虫脚本框架
这个网页爬取框架旨在为用户提供一种便捷的方法来收集网页资源，并提供一系列功能，包括获取网页信息、将网页保存为 PDF 格式、以及获取页面元素的 HTML 代码等  
> 在开始使用该脚本之前，请确保你使用的ChromeDriver版本支持你当前的Chrome浏览器版本,具体版本支持请参照ChromeDriver官网<https://chromedriver.chromium.org/>将下载的exe文件替换到``public``目录下

## 示例创建
访问百度官网且保存成pdf格式

    driver = Driver()
    driver.get_driver("Windows")
    driver.d.get("https://www.baidu.com")
    driver.save_pdf('demo.pdf')
    driver.close()


## 函数介绍
### ck_dir函数
用于检查指定的目录是否存在，如果不存在则创建该目录。
#### 参数
- *args: 可变数量的位置参数，用于指定路径的各个部分。
- file: 布尔型参数，可选，默认为False，指示是否创建文件夹而不是文件。
#### 返回值
str: 返回检查或创建后的路径

***

### Driver类
#### 类属性
type_dict: 字典类型，将字符串类型的定位方式映射到Selenium中对应的定位器
#### 类变量
d: uc.Chrome类型的变量，用于存储Selenium的WebDriver对象，默认值为None

***

### windows_driver方法
windows_driver方法用于配置和启动Chrome浏览器的WebDriver，以便使用Selenium进行网页操作
##### 参数
- c_sel_path：可选参数，表示ChromeDriver的路径。如果未提供，则使用默认路径
##### 详细说明
- 检查是否提供了c_sel_path参数，如果没有则使用默认路径
- 创建uc.ChromeOptions对象，并设置浏览器选项
- 创建一个字典settings，用于配置PDF打印选项
- 使用ck_dir函数创建一个下载路径，并将下载路径和其他选项添加到浏览器选项中
- 设置Chrome浏览器的DesiredCapabilities
- 使用uc.Chrome创建WebDriver对象，并将其保存在类的self.d属性中
##### 注意事项
请根据实际情况调整和修改默认路径和参数。

***

### get_driver方法
get_driver方法用于根据系统类型获取WebDriver，并进行相应的设置。
##### 参数
- sys：字符串类型，表示系统类型（如"windows"）
##### 详细说明
- 根据sys参数的值判断系统类型
- 如果系统类型是"windows"，调用windows_driver方法配置WebDriver，并将浏览器窗口最大化
- 使用set_window_size方法设置浏览器窗口大小为1920x1080，并最大化窗口（如果系统类型是"windows"）
- 返回配置好的WebDriver对象self.d
##### 注意事项
目前仅支持windows参数，无法适配Linux、MacOS系统

***

### close方法
close方法用于关闭WebDriver并清理资源
##### 详细说明
- 检查self.d是否存在
- 如果存在，使用close方法关闭当前窗口
- 使用quit方法退出WebDriver
- 删除self.d变量的引用并将其设置为None，以释放资源
##### 注意事项
请确保在不需要WebDriver对象时调用close方法以释放资源

***

### get_element方法
get_element方法用于根据指定的元素定位方式和标识符获取单个页面元素
##### 参数
- el_type：字符串类型，表示元素定位方式（如"class"、"id"、"xpath"、"name"）
- element：字符串或列表类型，表示要查找的元素标识符，可以是单个标识符或多个标识符
- err：布尔类型，表示是否抛出异常
- err_msg：字符串类型，表示异常信息
- t：整数类型，表示等待时间，默认为1
##### 返回值
WebElement：找到的页面元素对象
##### 详细说明
- 根据el_type获取对应的元素定位器
- 如果element是字符串，则使用find_element方法查找单个元素，并将命中选项添加到返回结果中
- 如果element是列表，则遍历列表中的每个标识符，逐个尝试查找元素，直到找到为止
- 如果设置了err参数且出现异常，则根据err_msg参数抛出异常，否则返回None
##### 注意事项
若一个元素中有多个标识符，则使用.隔开,如下放a标签  
`<a class="title-content  c-link c-font-medium c-line-clamp1">测试标签</a>`  
则传参格式为  
`driver.get_element('class','title-content.c-link.c-font-medium.c-line-clamp1')`

***

### get_elements方法
get_elements方法用于根据指定的元素定位方式和标识符获取多个页面元素
##### 参数
- el_type：字符串类型，表示元素定位方式（如"class"、"id"、"xpath"、"name"）
- element：字符串或列表类型，表示要查找的元素标识符，可以是单个标识符或多个标识符
- err：布尔类型，表示是否抛出异常，默认为False
- t：整数类型，表示最大尝试次数，默认为1
##### 返回值
WebElement：找到的页面元素对象列表
##### 注意事项
请参考get_element方法

***

### el_get_element方法
el_get_element方法用于在指定的页面元素对象中根据指定的元素定位方式和标识符获取单个页面元素
##### 参数
- el_obj：WebElement类型，表示要查找元素的页面元素对象
- el_type：字符串类型，表示元素定位方式（如"class"、"id"、"xpath"、"name"）
- element：字符串或列表类型，表示要查找的元素标识符，可以是单个标识符或多个标识符
如果设置了err参数且出现异常，则根据err_msg参数抛出异常，否则返回None
- t：整数类型，表示最大尝试次数，默认为1
##### 返回值
WebElement：找到的页面元素对象
##### 注意事项
请参考get_element方法

***

### el_get_elements方法
el_get_elements方法用于在指定的页面元素对象中根据指定的元素定位方式和标识符获取多个页面元素
##### 参数
- el_obj：WebElement类型，表示要查找元素的页面元素对象
- el_type：字符串类型，表示元素定位方式（如"class"、"id"、"xpath"、"name"）
- element：字符串或列表类型，表示要查找的元素标识符，可以是单个标识符或多个标识符
- err：布尔类型，表示是否抛出异常，默认为False
- t：整数类型，表示最大尝试次数，默认为1
##### 返回值
WebElement：找到的页面元素对象列表
##### 注意事项
请参考get_element方法

***

### send_element 方法
send_element 方法用于向指定的页面元素输入值
##### 参数
- el_type：字符串类型，表示元素定位方式（如 "class"、"id"、"xpath"、"name"）
- element：字符串类型，表示要查找的元素标识符
- text：字符串类型，表示要输入的文本值
- err_msg：字符串类型，表示异常信息，默认为空
- t：整数类型，表示最大尝试次数，默认为 1
##### 详细说明
- 根据 el_type 获取对应的元素定位器
- 使用 implicitly_wait 方法设置等待时间
- 使用 find_element 方法查找指定元素
- 使用 send_keys 方法向找到的元素输入文本值  
如果出现异常，根据 err_msg 参数抛出异常或返回默认异常信息

***

### del_element 方法
del_element 方法用于删除指定的页面元素
##### 参数
- el_type：字符串类型，表示元素定位方式（如 "class"、"id"、"xpath"、"name"）
- elements：列表类型，表示要删除的元素标识符列表
- el：WebElement 类型，表示父级元素，默认为 None
##### 详细说明
- 遍历 elements 列表中的每个元素标识符
- 如果提供了父级元素 el，则调用 el_get_elements 方法获取该父级元素下的指定元素
- 如果未提供父级元素 el，则调用 get_elements 方法获取当前页面中的指定元素
- 使用 JavaScript 执行删除操作，将找到的元素的 style.display 属性设置为 'none'，从而隐藏该元素

***

### check_title 方法
check_title 方法用于检查页面标题是否与指定标题匹配
##### 参数
- title：字符串类型，表示要检查的页面标题
- t：整数类型，表示最大尝试次数，默认为 10
##### 返回值
- True：如果页面标题与指定标题匹配
- 异常：如果超时未匹配到指定标题，则抛出异常
##### 详细说明
- 使用 WebDriverWait 方法等待页面标题出现，并设置超时时间为 1 秒
- 使用 EC.title_is 条件判断页面标题是否与指定标题匹配
- 如果匹配成功，则返回 True；如果超时未匹配到指定标题，则抛出异常

***

### screen_shot 方法
screen_shot 方法用于对当前页面进行截图并保存
##### 参数
- level：字符串类型，表示截图级别
- date：布尔类型，表示是否按日期存储，默认为 True
##### 返回值
file_path：字符串类型，表示截图文件的保存路径
##### 详细说明
- 调用 ck_dir 方法创建存储截图的目录
- 根据参数 level 拼接存储类型
- 如果设置了 date 参数为 True，则根据当前日期创建目录
- 使用 get_screenshot_as_file 方法对当前页面进行截图，并保存到指定路径
- 返回截图文件的保存路径

***

### send 方法
send 方法用于向浏览器发送命令并获取结果
##### 参数
- cmd：字符串类型，表示要发送的命令
- params：字典类型，表示命令的参数，默认为 None
##### 返回值
命令执行结果的字典
##### 详细说明
- 根据 cmd 和 params 构造命令体
- 使用 WebDriver 的 _request 方法发送 POST 请求，向浏览器发送命令
- 获取响应结果中的值并返回

*** 

### save_mhtml_file 方法
save_mhtml_file 方法用于保存当前页面的 MHTML 文件
##### 参数
- save_path：字符串类型，表示要保存的文件路径
##### 返回值
save_path：字符串类型，表示保存的文件路径
##### 详细说明
- 调用 send 方法发送 Page.captureSnapshot 命令，获取当前页面的快照
- 根据 save_path 创建文件夹
- 将快照数据写入 MHTML 文件
- 返回保存的文件路径
##### 注意事项
传入的 save_path 参数包含文件名和扩展名(xxx.nhtml)

***

### get_mhtml 方法
get_mhtml 方法用于获取当前页面的 MHTML 数据
##### 返回值
MHTML 数据的字符串
##### 详细说明
- 调用 send 方法发送 Page.captureSnapshot 命令，获取当前页面的快照
- 返回快照数据中的 MHTML 数据

***

### get_css_img 方法
get_css_img 方法用于从当前页面的 MHTML 数据中提取 CSS 和图片信息
##### 返回值
- css_lis：包含页面中所有 CSS 内容的列表
- img_dic：包含图片名称和对应内容的字典
- sav_bs：包含图片名称和对应 base64 编码的字典
##### 详细说明
- 将获取到的 MHTML 数据解析为 email.Message 对象
- 遍历 email.Message 对象的每个部分，根据 Content-Type 提取 CSS 和图片信息
- 将提取的 CSS 内容添加到 css_lis 列表中
- 将提取的图片内容添加到 img_dic 字典中，键为图片的 Content-Location，值为图片内容
- 将提取的图片内容转换为 base64 编码并添加到 sav_bs 字典中，键为图片的 Content-Location，值为 base64 编码
##### 注意事项
此方法依赖于 get_mhtml 方法，确保在调用前已正确实现该方法

***

### save_pdf 方法
save_pdf 方法用于将当前页面保存为 PDF 文件
##### 参数
- save_path：字符串类型，表示要保存的 PDF 文件路径
##### 返回值
- pdf_name：字符串类型，表示保存的 PDF 文件名
##### 详细说明
- 使用 send 方法发送 Page.printToPDF 命令，获取当前页面的 PDF 数据
- 解析命令执行结果中的 PDF 数据，并将其解码为二进制数据
- 调用 ck_dir 方法创建保存 PDF 文件的目录
- 将 PDF 数据写入指定路径的 PDF 文件中
##### 注意事项
传入的 save_path 参数包含文件名和扩展名(xxx.pdf)

***

### et_el_html 方法
get_el_html 方法用于获取指定元素的 HTML 代码，并包含应用的 CSS 样式
##### 参数
- element：WebElement 类型，表示要获取 HTML 代码的元素
##### 返回值
- 字符串类型，表示指定元素的 HTML 代码，包含应用的 CSS 样式
##### 详细说明
- 使用 execute_script 方法执行 JavaScript 代码
- JavaScript 代码获取指定元素的 computed 样式，并筛选出不同于默认样式的样式
- 将筛选后的样式应用到元素上
- 递归处理子元素，并将结果返回为包含样式的 HTML 代码

