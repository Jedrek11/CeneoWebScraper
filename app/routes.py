from app import app
from flask import render_template, redirect, url_for, request
from app import utils
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == 'POST':
        product_code = request.form.get('product_code')
        url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
        opinions_all = []
        while(url):
            print(url)
            respons = requests.get(url)
            if  respons.status_code == requests.codes.ok:
                page_dom = BeautifulSoup(respons.text, 'html.parser')
                opinions = page_dom.select("div.js_product-review")
                for opinion in opinions:
                    single_opinion = {}
                    for key, value in utils.selectors.items():
                        single_opinion[key] = utils.get_tag_content(opinion, *value)
                    opinions_all.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+utils.get_tag_content(page_dom,"a.pagination__next","href")
            except TypeError:
                url = None
        try:
            os.mkdir("./app/data")
            os.mkdir("./app/data/opinions")
        except FileExistsError:
            pass
        with open(f"./app/data/opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
            json.dump(opinions_all, jf, indent=4, ensure_ascii=False)
        return redirect(url_for('product', code=product_code))
    return render_template('extract.html.jinja')

@app.route('/products')
def products():
    return render_template('products.html.jinja')

@app.route('/product/<code>')
def product(code):
    opinions = pd.read_json(f"./app/data/opinions/{code}.json")
    return render_template('product.html.jinja', 
                           product_code=code, 
                           opinions=opinions.to_html(header=True,
                                                     table_id="opinions",
                                                     classes="table table-striped table-hover"))

@app.route('/charts')
def charts():
    return render_template('charts.html.jinja')

@app.route('/author')
def author():
    return render_template('author.html.jinja')