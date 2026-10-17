from flask import Flask, request, jsonify

app = Flask(__name__)


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify(error="用户名和密码不能为空"), 400
    if not 3 <= len(username) <= 20:
        return jsonify(error="用户名长度需为3~20"), 400
    if not 6 <= len(password) < 16:  # BUG1：应为 <= 16
        return jsonify(error="密码长度需为6~16"), 400
    if username == "admin" and password == "123456":
        return jsonify(token="fake-token"), 200
    return jsonify(error="用户名或密码错误"), 401


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id > 100:  # BUG2：缺少 user_id < 1 的判断，id=0 会返回成功
        return jsonify(error="用户不存在"), 404
    return jsonify(id=user_id, name=f"user{user_id}"), 200


@app.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    if product_id is None or quantity is None:
        return jsonify(error="参数缺失"), 400
    if not isinstance(quantity, int):
        return jsonify(error="quantity必须是整数"), 400
    if quantity < 1 or quantity >= 10:  # BUG3：应为 > 10，数量10被误拒
        return jsonify(error="购买数量需为1~10"), 400
    return jsonify(order_id=1001, product_id=product_id, quantity=quantity), 201


@app.get("/products")
def list_products():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)
    if page < 1:
        return jsonify(error="page必须>=1"), 400
    if size > 50:  # BUG4：缺少 size < 1 的校验，size=0 会返回成功
        return jsonify(error="size需为1~50"), 400
    return jsonify(page=page, size=size, items=[]), 200


if __name__ == "__main__":
    app.run(port=5000)