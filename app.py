from flask import Flask, render_template, request, Response, send_from_directory
import pandas as pd
import textwrap
import random

app = Flask(__name__)

gp = pd.read_csv('geneinfo_params.csv', index_col=0)
template = 'https://www.yeastgenome.org/locus/'


@app.route("/")
def home():
    data = list(gp.index)
    val = {'place_hold': random.choice(data)}
    return render_template('home.html', data=val)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/gene')
def gene():
    # TODO: delete the wrappers around the text and  the wrapper call itself
    wrapper = textwrap.TextWrapper(width=50)
    gene_req = request.args.get('text', '').upper()
    web = template
    if gene_req in gp.index:
        web = template + gp.loc[gene_req, 'sgd']
        word_list = 'Description:  ' + gp.loc[gene_req, 'desc']

    elif gene_req in gp.orf.values:
        web = template + gp.loc[gp.orf == gene_req, 'sgd'].values[0]
        word_list = 'Description:  ' + wrapper.fill(text=(gp.loc[gp.orf == gene_req, 'desc'].values[0]))

    else:
        word_list = wrapper.fill(text='No such gene in my Database')
        web = 'https://www.yeastgenome.org/'
        gene_req = 'the Database'

    data = [{
        'name': gene_req,
        'info': word_list,
        'web': web
    }]

    return render_template('gene.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
