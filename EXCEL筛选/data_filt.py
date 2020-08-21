import pandas as pd

path = 'E:\\可视化\\输出文档\\中文名\\N2S结算单位汇总.xlsx'
sheet_name = ['开通N2S结算单位', '订单相关结算单位', '账单相关结算单位']
my_filter = 'sales_name'
name_list = [
    '贺琳',     
'王雪纯',    
'向阳',      
'杨小兰' ,   
'钟思敏'   , 
'邹方玲' ,   
'黎月明' ,   
'卢翠香' ,   
'舒乐'  ,    
'祝梦婷' ,   
'李镇粤' ,   
'欧阳婷'  ,  
'张波'   ,   
'张小东' ,   
'蔡浩权' ,   
'贺根强'   ,  
'梁健森' ,   
'刘城林' ,   
'曾浩炫',    
'梁诗婷',    
'刘泽民',    
'彭英剑' ,   
'章振坤' ,   
'郑瀚'  ,    
'helin', 
'wangxuechun', 
'xiangyang', 
'yangxiaolan', 
'zhongsimin', 
'zoufangling', 
'liyueming', 
'lucuixiang', 
'shule', 
'zhumengting', 
'lizhenyue',    
'ouyangting',    
'zhangbo',      
'zhangxiaodong' ,   
'caihaoquan',    
'hegenqiang',     
'liangjiansen',    
'liuchenglin' ,   
'zenghaoxuan',    
'liangshiting',    
'liuzemin',    
'pengyingjian',    
'zhangzhenkun',    
'zhenghan',  
]


# 多个sheet要使用writer方法，否则只会保存最后一个sheet
writer = pd.ExcelWriter('./result.xlsx')

# 行中某列作为筛选项
def data_filt(data, sheet_name, my_filter):    
    frame = data[data[my_filter].isin(name_list)] # 先判断该行是否符合，再取出符合的数据
    frame.index = range(frame.shape[0]) # 重命名行索引
    try:
        frame.to_excel(writer, sheet_name = sheet_name, index = False)        
    except:
        print('保存结果文件失败')

def main(): 
    try:
        for name in sheet_name:
            ordata = pd.read_excel(path, sheet_name=name)
            data_filt(ordata, name, 'sales_name')
    except Exception as e:
        print('数据处理异常:{}'.format(e))        
    else:
        print('good end')
    finally:
        writer.save()
        writer.close()

if __name__ == "__main__":
    main()