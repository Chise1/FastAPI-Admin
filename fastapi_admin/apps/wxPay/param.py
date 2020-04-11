# -*- encoding: utf-8 -*-
"""
@File    : param.py
@Time    : 2020/4/11 10:26
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :请求参数
"""
#公众账号ID	是	String(32)	微信支付分配的公众账号ID（企业号corpid即为此appId）
appid :str="wxd678efh567hg6787"
#商户号	mch_id	是	String(32)	微信支付分配的商户号
mch_id:str="1230000109"
#设备号	device_info	否	String(32)	自定义参数，可以为终端设备号(门店号或收银设备ID)，PC网页或公众号内支付可以传"WEB"
device_info="WEB"
#随机字符串	nonce_str	是	String(32)		推荐随机数生成算法
nonce_str:str="5K8264ILTKCH16CQ2502SI8ZNMTM67VS"
# 签名	sign	是	String(32)		通过签名算法计算得出的签名值，详见签名生成算法
sign:str="C380BEC2BFD727A4B6845133519F3AD6"
#签名类型	sign_type	否	String(32)	MD5	签名类型，默认为MD5，支持HMAC-SHA256和MD5。
sign_type:str="MD5"
# 商品描述	body	是	String(128)	腾讯充值中心-QQ会员充值 商品简单描述，该字段请按照规范传递，具体请见参数规定
body:str="腾讯充值中心-QQ会员充值"

# 商品详情	detail	否	String(6000)	 	商品详细描述，对于使用单品优惠的商户，该字段必须按照规范上传，详见“单品优惠参数说明”
detail:str=""

# 商户订单号	out_trade_no	是	String(32)	20150806125346	商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|* 且在同一个商户号下唯一。详见商户订单号
out_trade_no="20150806125346"
# 标价币种	fee_type	否	String(16)	CNY	符合ISO 4217标准的三位字母代码，默认人民币：CNY，详细列表请参见货币类型
fee_type="CNY"
# 标价金额	total_fee	是	Int	88	订单总金额，单位为分，详见支付金额
total_fee=88#注意单位为分！！！
# 终端IP	spbill_create_ip	是	String(64)	123.12.12.123	支持IPV4和IPV6两种格式的IP地址。用户的客户端IP
spbill_create_ip="123.12.12.123"
# 交易起始时间	time_start	否	String(14)	20091225091010	订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则
time_start="20091225091010"
# 交易结束时间	time_expire	否	String(14)	20091227091010

# 订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。订单失效时间是针对订单号而言的，由于在请求支付的时候有一个必传参数prepay_id只有两小时的有效期，所以在重入时间超过2小时的时候需要重新请求下单接口获取新的prepay_id。其他详见时间规则time_expire只能第一次下单传值，不允许二次修改，二次修改系统将报错。如用户支付失败后，需再次支付，需更换原订单号重新下单。
# 建议：最短失效时间间隔大于1分钟
time_expire="20091227091010"
# 订单优惠标记	goods_tag	否	String(32)	WXG	订单优惠标记，使用代金券或立减优惠功能时需要的参数，说明详见代金券或立减优惠
# 通知地址	notify_url	是	String(256)	http://www.weixin.qq.com/wxpay/pay.php	异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
notify_url=""
# 交易类型	trade_type	是	String(16)	JSAPI JSAPI -JSAPI支付 NATIVE -Native支付 APP -APP支付 说明详见参数规定
trade_type:str="MWEB"
# 商品ID	product_id	否	String(32)	12235413214070356458058	trade_type=NATIVE时，此参数必传。此参数为二维码中包含的商品ID，商户自行定义。
product_id:str="12235413214070356458058"
# # 指定支付方式	limit_pay	否	String(32)	no_credit	上传此参数no_credit--可限制用户不能使用信用卡支付
# # 用户标识	openid	否	String(128)	oUpF8uMuAJO_M2pxb1Q9zNjWeS6o	trade_type=JSAPI时（即JSAPI支付），此参数必传，此参数为微信用户在商户对应appid下的唯一标识。openid如何获取，可参考【获取openid】。企业号请使用【企业号OAuth2.0接口】获取企业号内成员userid，再调用【企业号userid转openid接口】进行转换
# openid:str=""
# # 电子发票入口开放标识	receipt	否	String(8)	Y	Y，传入Y时，支付成功消息和支付详情页将出现开票入口。需要在微信支付商户平台或微信公众平台开通电子发票功能，传此字段才可生效
# receipt:str=""
# # +场景信息	scene_info	否	String(256) 该字段常用于线下活动时的场景信息上报，支持上报实际门店信息，商户也可以按需求自己上报相关信息。该字段为JSON对象数据，对象格式为{"store_info":{"id": "门店ID","name": "名称","area_code": "编码","address": "地址" }} ，字段详细说明请点击行前的+展开
# scence_info={"store_info" : {
# "id": "SZTX001",
# "name": "腾大餐厅",
# "area_code": "440305",
# "address": "科技园中一路腾讯大厦" }}

