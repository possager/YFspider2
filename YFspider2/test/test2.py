#_*_coding:utf-8_*_
import requests
import json
import re





# response=requests.get(url='http://woeser.middle-way.net/2011/05/blog-post_18.html')
response=requests.get(url='http://woeser.middle-way.net/2014/03/blog-post_5.html')
response.encoding='UTF-8'
# print response.text

Re_find_all_reply=re.compile(r'var items \= (\[.*?\])\;')
reply_list= Re_find_all_reply.findall(response.text)

datarow= eval(reply_list[0])
print datarow



# print reply_list[0]
# print str(reply_list[0])


# str_raw='''
# [{'id': '1366369982663632131', 'body': '看了让人伤心&#65292;把人当猴耍&#12290;这些道德沦丧&#12289;人性泯灭的摄影者想拍藏民沧桑的脸&#65292;反被人拍到饿狼扑食般的德性还洋洋自得&#65292;真是可怜&#65281;', 'timestamp': '1305782797004', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1305782797004#c1366369982663632131', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年5月19日 下午1:26', 'deleteclass': 'item-control blog-admin pid-983113152'}, {'id': '1388366995853609718', 'body': 'ས&#3962;མས&#3851;པ&#3851;ས&#3984;&#4017;&#3964;&#3851;ས&#3964;ང&#3851;&#3853;', 'timestamp': '1305783588338', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1305783588338#c1388366995853609718', 'author': {'name': 'ཟ&#4019;&#3851;བ&#3851;གཞ&#3964;ན&#3851;ན&#3956;&#3853;', 'avatarUrl': '//3.bp.blogspot.com/_GpOkMRbeAnA/S_EEBU3-b0I/AAAAAAAAAAk/gSmlwP2CqZ8/S45-s35/kyab.jpg', 'profileUrl': 'https://www.blogger.com/profile/04184556303291763526'}, 'displayTime': '2011年5月19日 下午1:39', 'deleteclass': 'item-control blog-admin pid-1307728182'}, {'id': '4421449238143212582', 'body': '唉&#65292;一群丧失了摄影者基本道德的**&#65292;丢人啊&#65374;&#65374;&#65374;', 'timestamp': '1305830368959', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1305830368959#c4421449238143212582', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年5月20日 上午2:39', 'deleteclass': 'item-control blog-admin pid-1461216626'}, {'id': '7063236008094391084', 'body': '曾经&#65292;我也哭了&#12290;\x3cbr /\x3e\x3cbr /\x3e当我看到我心爱的舞者&#65292;在表演后被排成长长一个队伍的粉丝逐一要求合照&#65292;围绕着她不停说话&#65292;完全没有给她一个休息和喝水的空间&#12290;', 'timestamp': '1305877506578', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1305877506578#c7063236008094391084', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年5月20日 下午3:45', 'deleteclass': 'item-control blog-admin pid-1611500995'}, {'id': '7495664170069909856', 'body': '这些拍友很操蛋', 'timestamp': '1306083941676', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1306083941676#c7495664170069909856', 'author': {'name': '巴地斯圖塔', 'avatarUrl': '//lh3.googleusercontent.com/zFdxGE77vvD2w5xHy6jkVuElKv-U9_9qLkRYK8OnbDeJPtjSZ82UPq5w6hJ-SA\x3ds35', 'profileUrl': 'https://www.blogger.com/profile/15505869587252413812'}, 'displayTime': '2011年5月23日 上午1:05', 'deleteclass': 'item-control blog-admin pid-160353325'}, {'id': '6553186019025167009', 'body': '有無搞錯啊\x3cbr /\x3e這完全不尊重人', 'timestamp': '1306639176549', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1306639176549#c6553186019025167009', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年5月29日 上午11:19', 'deleteclass': 'item-control blog-admin pid-2120076261'}, {'id': '1735196682876715093', 'body': 'འད&#3954;&#3851;ལ&#3999;ར&#3851;མཐ&#3964;ང&#3851;ཆ&#3956;ང&#3851;བ&#4017;&#3962;ད&#3851;བཞ&#3954;ན&#3851;པ&#3851;མཐ&#3964;ང&#3851;ན&#3851;ང&#3964;&#3851;མ&#3851;ས&#3962;མས&#3851;མ&#3954;&#3851;བད&#3962;&#3851;ཀ&#3954; ཁ&#3964;ང&#3851;ཚ&#3964;ས&#3851;འཇ&#3954;ག&#3851;ར&#3999;&#3962;ན&#3851;མ&#4017;&#3954;&#3851;ཞ&#3954;ག&#3851;དང&#3851;ད&#3962;&#3851;ལ&#3851;དགའ&#3851;ས&#3984;&#4017;&#3964;&#3851;ཆགས&#3851;ས&#4001;ང&#3851;ག&#3954;&#3851;ཚ&#3964;ར&#3851;བ&#3851;ཡ&#3964;ད&#3851;པ&#3851;བསམ&#3851;བ&#4019;&#3964;&#3851;བཟང&#3851;མ&#3954;&#3851;འད&#3956;ག', 'timestamp': '1307004913714', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1307004913714#c1735196682876715093', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年6月2日 下午4:55', 'deleteclass': 'item-control blog-admin pid-935477394'}, {'id': '3981688913395869110', 'body': '每年春节后&#65292;从大年初13到16号在郎木寺的2个寺院里有有很大的宗教活动&#65292; 大批来自内地的摄影师挡住朝圣者的路拍照&#65292;当地人其实很讨厌被拍的&#65292;但是那些没有一点道德素质的游人或摄影师们就是要拍&#65292; 想象一下如果我们在他们的城市在他们工作的地方拿着照相机拍摄&#65292;可能我们早已被侵犯某人的肖像权而定罪了&#65292; 我讨厌那些人到郎木寺来&#65292;在我刚懂事时&#65292;那里没有被污染成那样&#65292;随之所谓的中国经济增长&#65292;汉人以各种方式进入我的家乡&#65292;而我们没有办法阻止他们', 'timestamp': '1307623125613', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1307623125613#c3981688913395869110', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2011年6月9日 下午8:38', 'deleteclass': 'item-control blog-admin pid-735352183'}, {'id': '398297468051829302', 'body': '说真的&#183;&#183;&#183;我们都已经习惯了&#183;他们从来不会尊重我们&#12290;也难怪&#183;&#183;这又不是他们的家&#12290;一个旅客住店当然不会去珍惜里面的设施&#183;&#183;', 'timestamp': '1372702474921', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1372702474921#c398297468051829302', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2013年7月2日 上午2:14', 'deleteclass': 'item-control blog-admin pid-37588573'}, {'id': '2829769677626274068', 'body': '好几年前的事情了  我也是摄影人  感到真可耻 那些人怎不去死一死 真他妈丢脸', 'timestamp': '1384409680309', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1384409680309#c2829769677626274068', 'author': {'name': '冷非顏', 'avatarUrl': '//lh3.googleusercontent.com/zFdxGE77vvD2w5xHy6jkVuElKv-U9_9qLkRYK8OnbDeJPtjSZ82UPq5w6hJ-SA\x3ds35', 'profileUrl': 'https://www.blogger.com/profile/03672396480755194365'}, 'displayTime': '2013年11月14日 下午2:14', 'deleteclass': 'item-control blog-admin pid-588411484'}, {'id': '3332736905934800178', 'body': '对野生动物都不会这样&#65292;好夸张&#12290;看了这篇&#65292;我决定日后进藏除了保护自己的需要外&#65292;绝不对藏人拍照摄影&#12290;', 'timestamp': '1385394255676', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1385394255676#c3332736905934800178', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2013年11月25日 下午11:44', 'deleteclass': 'item-control blog-admin pid-247919320'}, {'id': '3389918443644997156', 'body': '我们汉人就是这样帮助&#65292;发展藏民族&#65311;我感到羞愧&#12290;', 'timestamp': '1393468109663', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1393468109663#c3389918443644997156', 'author': {'name': '匿名', 'avatarUrl': '//img1.blogblog.com/img/blank.gif', 'profileUrl': ''}, 'displayTime': '2014年2月27日 上午10:28', 'deleteclass': 'item-control blog-admin pid-1833469676'}, {'id': '3838303850604471752', 'body': '在一个人权被肆意践踏的国度&#65292;没有尊严地苟活着&#65281;', 'timestamp': '1464844731647', 'permalink': 'http://woeser.middle-way.net/2011/05/blog-post_18.html?showComment\x3d1464844731647#c3838303850604471752', 'author': {'name': 'kangny', 'avatarUrl': '//lh3.googleusercontent.com/zFdxGE77vvD2w5xHy6jkVuElKv-U9_9qLkRYK8OnbDeJPtjSZ82UPq5w6hJ-SA\x3ds35', 'profileUrl': 'https://www.blogger.com/profile/06936956080605611197'}, 'displayTime': '2016年6月2日 下午1:18', 'deleteclass': 'item-control blog-admin pid-119815395'}]
# '''
#
# str_raw_int=list(eval(str_raw))
# print str_raw_int


def deal_reply_nodes(reply_nodes=None):
    reply_nodes_list = []

    def deal_publishtime_inside(publishtime):
        publish_time = publishtime.replace('年', '-').replace('月', '-').replace('日', '')
        time_split_2 = publish_time.split(' ')

        data_str = time_split_2[0]
        data_str_list = data_str.split('-')
        mounth = data_str_list[1]
        day = data_str_list[2]
        if len(mounth) < 2:
            mounth = '0' + mounth
        if len(day) < 2:
            day = '0' + day
        data_str = data_str_list[0] + '-' + mounth + '-' + day

        time_split_2_part2 = time_split_2[1]
        if '下午' in time_split_2_part2:
            time_part2_h_m = time_split_2_part2.replace('下午', '').split(':')
            time_split_2_h = int(time_part2_h_m[0])
            time_split_2_m = time_part2_h_m[1]
            time_split_2_h_add = 12 + time_split_2_h

            time_pm_finally = str(time_split_2_h_add) + ':' + time_split_2_m + ':00'
            return data_str + ' ' + time_pm_finally
        elif '上午' in time_split_2_part2:
            time_part2_h_m = time_split_2_part2.replace('上午', '').split(':')
            time_split_2_h = int(time_part2_h_m[0])
            time_split_2_m = time_part2_h_m[1]
            time_split_2_h_add = time_split_2_h

            if time_split_2_h_add < 10:
                time_split_2_h_add = '0' + str(time_split_2_h)

            time_am_finally = str(time_split_2_h_add) + ':' + time_split_2_m + ':00'
            return data_str + ' ' + time_am_finally

    if reply_nodes:
        reply_nodes_list_eval = eval(reply_nodes)
        for one_reply_nodes in reply_nodes_list_eval:
            content = one_reply_nodes['body']
            publish_time_raw = one_reply_nodes['displayTime']
            publish_time = deal_publishtime_inside(publish_time_raw)

            id = one_reply_nodes['id']
            publish_user_photo = one_reply_nodes['author']['avatarUrl']
            publish_user = one_reply_nodes['author']['name']

            child_reply_node = {
                'content': content,
                'publish_time': publish_time,
                'id': id,
                'publish_user_href': publish_user_photo,
                'publish_user': publish_user
            }
            reply_nodes_list.append(child_reply_node)

        return reply_nodes_list
    else:
        return None

print deal_reply_nodes(reply_list[0])