from selenium import webdriver
import time
import csv

# 创建浏览器对象
driver = webdriver.Chrome()
# 访问京东
url = 'https://www.jd.com/'
driver.get(url)
# 接收终端输入,向搜索框发内容
key = input('输入搜索商品:')
driver.find_element_by_class_name('text').send_keys(key)
# 点击搜索按钮
driver.find_element_by_class_name('button').click()
time.sleep(2)

for i in range(5):
    # 执行JS脚本,把进度条拉到最底部
    driver.execute_script(
        'window.scrollTo(0,document.body.scrollHeight)'
    )
    time.sleep(2)

    # 获取商品信息列表,遍历出来
    rList = driver.find_elements_by_xpath \
        ('//div[@id="J_goodsList"]/ul/li')
    print(rList)
    for r in rList:
        # text属性可获取子节点和后代节点的文本内容
        info = r.text.split('\n')
        if info[1] == '拍拍':
            price = info[0]
            name = info[2]
            commit = info[3]
            shop = info[4]
        else:
            price = info[0].strip()
            name = info[1].strip()
            commit = info[2].strip()
            shop = info[3].strip()

        d = {
            'price': price,
            'name': name,
            'commit': commit,
            'shop': shop
        }
        with open('京东爬虫数据.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([price,name,commit,shop])

    # 是否点击下一页
    if driver.page_source.find('pn-next disabled') == -1:
        driver.find_element_by_class_name('pn-next').click()
        time.sleep(2)
    else:
        break

driver.quit()










