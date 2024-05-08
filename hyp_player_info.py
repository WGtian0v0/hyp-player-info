import cloudscraper
from bs4 import BeautifulSoup

name = "在这里输入名字"
url = 'https://plancke.io/hypixel/player/stats/{}#BedWars'.format(name)


# 伪装一下
scraper = cloudscraper.create_scraper(browser={
    'browser': 'firefox',
    'platform': 'windows',
    'mobile': False
})
res = scraper.get(url)
response = res.text
soup = BeautifulSoup(response, "html.parser")


# 大厅信息数据
def lobby_info():
    info = soup.findAll("div", {"class": "card-box m-b-10"})
    info_str = ""
    for i in info:
        info_str += i.get_text("<br>")
    info_list = info_str.split("<br>")
    info_list = [x for x in info_list if x != "\n" and x != " "]
    # 大厅等级和状态(可增添、修改，详情看 info_list)
    for i in range(len(info_list)):
        if info_list[i] == "Level:":
            lobby_level = info_list[i + 1]
        if info_list[i] == "Status":
            status = info_list[i + 1]

    return lobby_level, status


# 起床战争数据
def bedwars_info():
    text = soup.findAll({"div"}, {"id": "stat_panel_BedWars"})
    bedwar_list_str = ""
    for d in text:
        bedwar_list_str += d.get_text("<b>")
    bedwar_list = bedwar_list_str.split("<b>")
    bedwar_list = [x for x in bedwar_list if x != "\n" and x != " "]
    # 起床等级(可增添、修改，详情看 bedwar_list)
    for i in range(len(bedwar_list)):
        if bedwar_list[i] == "Level:":
            bedwar_level = bedwar_list[i + 1]

    # 各模式具体数据(可增添、修改，详情看 bedwar_list)
    # K  D  K/D(Normal) 	K  D  K/D(Final) 	 W  L  W/L    Beds Broken
    # 1  2   3              4  5   6             7  8   9         10
    for i in range(len(bedwar_list)):
        if bedwar_list[i] == "Overall":
            KD = bedwar_list[i + 3]
            WL = bedwar_list[i + 9]
            beds_broken = bedwar_list[i + 10]

    return bedwar_level, KD, WL, beds_broken


# 判断是否请求成功
if res.ok:
    lobby_info()
    bedwars_info()
else:
    print("请求错误")