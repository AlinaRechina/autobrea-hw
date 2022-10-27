from flask import Flask, request, render_template
from unholy5 import *

app = Flask(__name__)

@app.route("/")
@app.route("/main")
def main_page():
    return render_template("main.html")

@app.route("/result")
def result():
    query = request.args.get('query')
    answer = make_beautiful_print(wordowski_search(making_whole_pattern(query)[0], 
                                                   making_whole_pattern(query)[1]))
    if type(answer) != list:
        answer = [["",["Извините, по вашему запросу ничего не найдено.", "", ""]]]
    return render_template("query.html", answer=answer)

@app.route("/instruction")
def instruction():
    return render_template("instruction.html")

if __name__ == '__main__':
    app.run(debug=True) # НЕ ЗАБЫТЬ УБРАТЬ