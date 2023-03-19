from pyecharts.charts import Page, Sankey
from pyecharts import options as opts
import pandas as pd
# 读取csv文件
data = pd.read_excel('key_value.xlsx')
# 生成nodes
nodes = []
# 在第一列"source"中查找添加节点名称
for i in data.iloc[:,0].unique():
    dic = {'name': i}
    nodes.append(dic)
# 在第二列"target"中查找添加节点名称
for i in data.iloc[:,1].unique():
    dic = {'name': i}
    if dic not in nodes:
        nodes.append(dic)
#生成links1
links = []
for i in data.values:
    if i[2] >= 0.67:
        i[2] *= 10000
    else:
        #i[2] *= 0
        continue


    dic = {'source': i[0], 'target': i[1], 'value': i[2]}
    links.append(dic)
print(links)
# 读取数据中的标题、副标题和图例名称
# 生成可视化结果
c = (
    Sankey()
        .add(
        "senkey",
        nodes,
        links,
        # 设置主图在图片区域的相对位置
        pos_top="10%", pos_bottom="5%", pos_right="10%", pos_left="5%",

        # 桑基图中每个矩形节点的宽度,每一列任意两个矩形节点之间的间隔，
        # 节点的对齐方式，默认是双端对齐，可以设置为左对齐或右对齐，对应的值分别是"left""right""justify"
        node_width=20, node_gap=5, node_align="left",

        # 桑基图中节点的布局方向，可以是水平的从左往右，也可以是垂直的从上往下。
        # 对应的参数值分别是 horizontal, vertical。
        orient="horizontal",

        # 控制节点拖拽的交互，默认开启。开启后，用户可以将图中任意节点拖拽到任意位置。若想关闭此交互，只需将值设为 false 就行了。
        is_draggable=True,
        # 鼠标 hover 到节点或边上，相邻接的节点和边高亮的交互，默认关闭，可手动开启。
        # false：hover 到节点或边时，只有被 hover 的节点或边高亮。
        # true：同 'allEdges'。
        # 'allEdges'：hover 到节点时，与节点邻接的所有边以及边对应的节点全部高亮。hover 到边时，边和相邻节点高亮。
        # 'outEdges'：hover 的节点、节点的出边、出边邻接的另一节点 会被高亮。hover 到边时，边和相邻节点高亮。
        # 'inEdges'：hover 的节点、节点的入边、入边邻接的另一节点 会被高亮。hover 到边时，边和相邻节点高亮。
        focus_node_adjacency=True,
        # 线条样式配置项，
        linestyle_opt=opts.LineStyleOpts(opacity=0.4,
                                         # 图形透明度。支持从 0 到 1 的数字，为 0 时不绘制该图形。

                                         curve=0.4,
                                         # 线的弯曲度，0 表示完全不弯曲

                                         color="source",
                                         type_="dotted"),
        # 线的类型。可选：'solid', 'dashed', 'dotted'

        label_opts=opts.LabelOpts(position="right",
                                  # 标签的位置。可选
                                  # 'top'，'left'，'right'，'bottom'，'inside'，'insideLeft'，'insideRight'
                                  # 'insideTop'，'insideBottom'， 'insideTopLeft'，'insideBottomLeft'
                                  # 'insideTopRight'，'insideBottomRight'

                                  # 文字的字体大小
                                  font_size=12,

                                  ), )
        .set_global_opts(
        # 设置标题和副标题
        title_opts=opts.TitleOpts(title='senkey', subtitle='senkey'),

        tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),

        # 是否显示图例
        legend_opts=opts.LegendOpts(is_show=True,
                                    item_width=15, item_height=14,
                                    legend_icon="pin",

                                    # 右侧靠齐
                                    pos_right="5%", )
    )
)
c.render('sankey.html')