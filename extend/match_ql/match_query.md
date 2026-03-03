
# query查询表达式-参数获取工具

## 说明
~~~
代码内实现方式, 见demo模块: SampleRepo.index() 和 SampleRepo.read()方法.
以下内容为 该工具的 接口调用规范.
~~~

### 接口调用规范
~~~
如果是自动生成的接口代码, 且执行主表自定义查询, 都默认支持下面这些查询query.
~~~


### POST 类型接口
~~~
没有特别规定
~~~


### GET 类型接口
~~~
get接口若要开启临时缓存, 统一添加query参数: '_time'. 约定不传该参数时,默认调用缓存 ; 传 '_time=1' 时, 跳过缓存.
~~~


#### * 获取-列表-实时 & 获取-详情-实时 "_time":
~~~
{{base_url}}/demo/sample/index ?_time=1
{{base_url}}/demo/sample/read/1 ?_time=1
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _time | _time=1 | 跳过缓存: 不跳过=0,跳过=1, 默认不跳过. |


#### * 获取-列表-翻页 "_pagination,_page,_page_size":
~~~
{{base_url}}/demo/sample/index ?_pagination=true &_page=1 &_page_size=3
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _pagination | _pagination=true | 翻页 打开=true,关闭=false; 关闭时,一页100条数据上限; 默认20; |
| _page | _page=1 | 页码 默认1 |
| _page_size | _page_size=3 | 页数 默认20 |


#### * 获取-列表-关联副表数据 "_include":
~~~
{{base_url}}/demo/sample/index ?_include=image,video
----------------------------------------
_include=? 关联数据: 按场景选择需关联对象,提高接口性能.
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _include | _include=image,video | 指定关联模型 关联 image,video 数据, 需要服务端定制; |


#### * 获取-列表-筛选动作 "_search" :
~~~
{{base_url}}/demo/sample/index ?_search=demo &type=1 &status=1,2 &name=陈%
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _search | _search=demo | 触发demo模块"主表筛选动作", 默认值对应实际api根路径名, 所以这里是'demo'. 若有其它筛选动作,再增加动作名称. |
| type | type=1 |  触发"主表筛选动作时", 添加 type = 1 的筛选条件, '=,>,<,>=,<='运算符,服务端内部设定,前端不用关心. 字段名对应表字段. |
| status | status=1,2 | 触发"主表筛选动作"时, 添加 status in 1,2 的筛选条件, 即包含条件. 字段名对应表字段. |
| name | name=陈% |  触发"主表筛选动作"时, 添加 name like 陈% 的筛选条件, 即"陈"开头的姓名. 字段名对应表字段. |


#### * 获取-列表-副表扩展查询 "_extend":
~~~
{{base_url}}/demo/sample/index ?_extend=user &user_type=1 &user_status=1 ...
----------------------------------------
_extend=? 副表查询动作: 按需要触发.
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _extend | _extend=user | 扩展查询副表-user, 需要服务端定制; |
| user_type,user_status ... | &user_type=1 &user_status=1 ... | 触发 "扩展查询副表-user" 时, 传递的副表查询参数, 进行副表字段查询, 需要服务端定制; |


#### * 获取-列表-排序 "_sort":
~~~
{{base_url}}/demo/sample/index ?_sort=-id
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _sort | _sort=-id | 自定义排序, 升序= id , 倒序= -id ; 默认倒序, id可以是其它字段; |
| _sort | _sort=-id,-num | 自定义排序, 升序= id , 倒序= -id ; 默认倒序, id可以是其它字段; 支持多个字段 |


#### * 获取-列表-分组 "_group":
~~~
{{base_url}}/demo/sample/index ?_group=city_id,user_id
~~~
| 字段 | 示例 | 说明 |
| --- | --- | --- |
| _group | _group=city_id | 按"城市"分组, city_id可以是其它字段; |
| _group | _group=city_id,user_id | 按"城市->用户"分组, city_id,user_id可以是其它字段; 支持多个字段. |

