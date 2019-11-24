import numpy as np
import os
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import json



def prepD():
    engine = create_engine("sqlite:///db/bellybutton.sqlite")
    conn = engine.connect()
    inspector = inspect(engine)


    Base = automap_base()
    Base.prepare(engine, reflect=True)

    Sample_metadata = Base.classes.sample_metadata
    Samples = Base.classes.samples
    session = Session(engine)

    sample_data = pd.read_sql("SELECT * FROM samples",conn)
    metadata = pd.read_sql("SELECT * FROM sample_metadata",conn)

    sample_datax = sample_data.set_index(["otu_id","otu_label"])
    # print(sample_data)
    # print(metadata)
    return sample_datax, metadata

