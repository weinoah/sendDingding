import requests
from bs4 import BeautifulSoup
 
 
def getHTMLText(url,timeout = 30):
    try:
        r = requests.get(url, timeout = 30)       #用requests抓取网页信息
        r.raise_for_status()                      #可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'
    
 
def get_data(html):
    final_list = []
    soup = BeautifulSoup(html,'html.parser')       #用BeautifulSoup库解析网页
    body  = soup.body
    data = body.find('div',{'id':'7d'})
    ul = data.find('ul')
    lis = ul.find_all('li')
 
 
    for day in lis:
        temp_list = []
        
        date = day.find('h1').string             #找到日期
        temp_list.append(date)     
    
        info = day.find_all('p')                 #找到所有的p标签
        temp_list.append(info[0].string)
    
        if info[1].find('span') is None:          #找到p标签中的第二个值'span'标签——最高温度
            temperature_highest = ' '             #用一个判断是否有最高温度
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃',' ')
            
        if info[1].find('i') is None:              #找到p标签中的第二个值'i'标签——最高温度
            temperature_lowest = ' '               #用一个判断是否有最低温度
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃',' ')
            
        temp_list.append(temperature_highest)       #将最高气温添加到temp_list中
        temp_list.append(temperature_lowest)        #将最低气温添加到temp_list中
    
        wind_scale = info[2].find('i').string      #找到p标签的第三个值'i'标签——风级，添加到temp_list中
        temp_list.append(wind_scale)
    
        final_list.append(temp_list)              #将temp_list列表添加到final_list列表中
#    print(final_list)
    return final_list
    
#用format()将结果打印输出
def print_data(final_list,num):
    print("{:^8}\t{:^6}\t{:^6}\t{:^6}\t{:^6}".format('日期','天气','最高温','最低温','风级'))
    for i in range(num):    
        final = final_list[i]
        print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format(final[0],final[1],final[2],final[3],final[4]))


def table_data(final_list):
    for i in range(len(final_list)):
        final_list[i] = "{:^8}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format(final_list[i][0],final_list[i][1],final_list[i][2],final_list[i][3],final_list[i][4])
#    table_head = "{:^8}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format('日期','天气','最高温度','最低温度','风级')
#    final_list.insert(0,table_head)
    return  final_list


#用main()主函数将模块连接
def main():
    url = 'http://www.weather.com.cn/weather/101280601.shtml'
    html = getHTMLText(url)
    final_list = get_data(html)
    print(final_list[0][1])
    print_data(final_list,7)
    table_data(final_list)
main()
