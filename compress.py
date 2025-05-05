import pickle
import gzip
with open("similarity.pkl","rb") as f_in:
    with gzip.open("similarity_compressed.pkl.gz","wb") as f_out:
        f_out.write(f_in.read())