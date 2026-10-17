BASE_URL = "http://127.0.0.1:5000"

API_SPEC = [
    {
        "name": "用户登录",
        "method": "POST",
        "path": "/login",
        "body": "JSON：username、password",
        "rules": "用户名和密码均不能为空，否则返回400；"
                 "用户名长度3~20，密码长度6~16，超出范围返回400；"
                 "用户名admin且密码123456登录成功返回200；"
                 "其他用户名密码组合返回401",
    },
    {
        "name": "查询用户",
        "method": "GET",
        "path": "/users/{user_id}",
        "body": "无",
        "rules": "user_id为整数，范围1~100时返回200；"
                 "范围外返回404",
    },
    {
        "name": "创建订单",
        "method": "POST",
        "path": "/orders",
        "body": "JSON：product_id、quantity",
        "rules": "两个参数都必填，缺少返回400；"
                 "quantity必须是整数，否则返回400；"
                 "quantity范围1~10，成功返回201，范围外返回400",
    },
    {
        "name": "商品列表",
        "method": "GET",
        "path": "/products",
        "body": "无，查询参数：page、size",
        "rules": "page默认1，必须>=1，否则返回400；"
                 "size默认10，范围1~50，超出返回400；"
                 "合法时返回200",
    },
]