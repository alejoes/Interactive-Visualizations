import numpy as np
import os
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import prep

from flask import Flask, render_template, url_for, jsonify, request

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/sample")
# def sample():
#     datax = pd.read_sql("SELECT * FROM samples",conn)
#     return(datax.head())

@app.route("/names")
def namesF():
    return_data = prep.prepD()
    sample_data = return_data[0]
    
    sampl = list(sample_data.columns)
    return jsonify(sampl)

@app.route("/samples/<sample>")
def sample(sample):
    return_data = prep.prepD()
    sample_data = return_data[0]
    filtered_DF = sample_data[[sample]]               #aqui meto el sample
    final_df = filtered_DF.loc[~(filtered_DF==0).all(axis=1)]

    final_df = final_df.reset_index()

    total_sum = final_df[sample].sum()
    final_df['porcentage'] = 100*final_df[sample]/final_df[sample].sum()
    top_Ten = final_df.nlargest(10,sample)

    otu_id = top_Ten['otu_id'].tolist()
    otu_label = top_Ten['otu_label'].tolist()
    values = top_Ten[sample].tolist()
    porcent = top_Ten["porcentage"].tolist()
    myList = [round(x) for x in porcent]


    data_dic = {
        "otu_id" : otu_id, 
        "sample_values" : values, 
        "out_label" : otu_label, 
        "Percentage" : myList
    }
    return jsonify(data_dic)


@app.route("/metadata/<int:sample>")
def metad(sample):
    return_data = prep.prepD()
    metadata = return_data[1]
    
    selection = metadata[metadata["sample"] == sample]
    # print(selection)
    ethn = selection["ETHNICITY"].to_list()[0]
    age = int(selection["AGE"].to_list()[0])
    bbt = selection["BBTYPE"].to_list()[0]
    gnd = selection["GENDER"].to_list()[0]
    loca = selection["LOCATION"].to_list()[0]
    wfr = int(selection["WFREQ"].to_list()[0])
    samp = selection["sample"].to_list()[0]

    meda_dict = {
        "Age": age,
        "BBTYPE": bbt,
        "Ethnicity": ethn,
        "Gender": gnd,
        "Location": loca,
        "WFreq": wfr,
        "Sample": samp
    }
    # print(jsonify(meda_dict))
    return jsonify(meda_dict)

if __name__ == "__main__":
    app.run()

    
