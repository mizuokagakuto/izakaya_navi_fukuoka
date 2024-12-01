from flask import Flask, render_template, request, redirect, url_for, session
from calculation import calculate_weightedsum
from flask_session import Session
from redis import Redis
import os

app = Flask(__name__)
"""
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_REDIS"] = Redis(
    host="your_redis_host", port=6379, password="your_password"
)
Session(app)
"""
app.config["SECRET_KEY"] = "your_secret_key"  # セッションデータ暗号化用のキー
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Redisクライアントを作成
redis_client = Redis.from_url(redis_url)  # Flask-Sessionの設定
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis_client
Session(app)


@app.route("/")
def index():
    session["click_count"] = 0
    return render_template("index.html")


# --------------------------------------#
@app.route("/calc", methods=["GET", "POST"])
def calculation():
    if request.method == "GET":
        session["click_count"] = 0
        return render_template("calculation.html")
    elif request.method == "POST":
        session["click_count"] = 0
        pozi_nega_rank = request.form["pozi_nega_rank"]
        satisfy_rank = request.form["satisfy_rank"]
        insta_rank = request.form["insta_rank"]
        calm_rank = request.form["calm_rank"]
        service_rank = request.form["service_rank"]
        star_rank = request.form["star_rank"]

        money = request.form["money"]
        place = request.form["place"]

        weights = {
            "star_score_re": star_rank,
            "posi_nega_score_re": pozi_nega_rank,
            "satisfy_score_re": satisfy_rank,
            "insta_score_re": insta_rank,
            "calm_score_re": calm_rank,
            "service_score_re": service_rank,
        }
        # 計算結果をセッションに保存
        session["weights"] = weights
        session["money"] = money
        session["place"] = place

        # /result にリダイレクト
        return redirect(url_for("result"))


# --------------------------------------#
@app.route("/result")  # , methods=["GET", "POST"])
def result():
    session["click_count"] = 0

    weights = session.get("weights", {})
    money = session.get("money", "No result available")
    place = session.get("place", "No result available")

    output = calculate_weightedsum(
        weights, max_money=money, place=place, count=session["click_count"]
    )
    return render_template("result.html", output=output, count=session["click_count"])


@app.route("/result_more", methods=["POST"])  # クリックして結果を更新
def result_more():
    # クリック数を増加
    session["click_count"] += 10
    count = session["click_count"]

    weights = session.get("weights", {})
    money = session.get("money", "No result available")
    place = session.get("place", "No result available")

    # 重み付き計算
    output = calculate_weightedsum(weights, max_money=money, place=place, count=count)

    # 結果を表示
    return render_template("result.html", output=output, count=count)


@app.route("/result_less", methods=["POST"])  # クリックして結果を更新
def result_less():
    # クリック数を増加
    session["click_count"] -= 10
    count = session["click_count"]

    weights = session.get("weights", {})
    money = session.get("money", "No result available")
    place = session.get("place", "No result available")

    # 重み付き計算
    output = calculate_weightedsum(weights, max_money=money, place=place, count=count)

    # 結果を表示
    return render_template("result.html", output=output, count=count)


if __name__ == "__main__":
    app.run(debug=False)
