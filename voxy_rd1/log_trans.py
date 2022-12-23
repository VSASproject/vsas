import pandas as pd
import numpy as np

br_1=[22472.16, 20810.28, 18896.76, 17170.92, 15405.0, 13750.68, 12319.2, 10938.12, 9661.2, 8594.64, 7575.48, 6587.16, 5698.32, 4931.04, 4206.72, 3716.76, 3219.24, 2731.44, 2369.88, 2073.84, 1867.8]
br_3=[31176.96, 28968.0, 26567.64, 24409.68, 22195.68, 20082.84, 18108.72, 16231.8, 14428.44, 12785.76, 11491.68, 9916.68, 8676.24, 7537.92, 6533.52, 5765.28, 4966.32, 4212.96, 3622.56, 3117.6, 2746.2]
br_10=[31176.96, 28968.0, 26567.64, 24409.68, 22195.68, 20082.84, 18108.72, 16231.8, 14428.44, 12785.76, 11491.68, 9916.68, 8676.24, 7537.92, 6533.52, 5765.28, 4966.32, 4212.96, 3622.56, 3117.6, 2746.2]

def save_one(Dr):
    p1 = "data/aqp_dr_psnr1.csv"
    df = pd.read_csv(p1)

    if Dr == 0.1:
        df2 = df[df.Dr == Dr]
        df2 = df2.reset_index()
        db = pd.DataFrame({"BR": br_1})
        print(db)
        df2 = df2.join(db)
        print(df2)
        df2.to_csv("data/" + "aqp" + str(int(100 * Dr)) + ".csv", index=False)
    elif Dr == 0.33:
        df2= df[df.Dr == Dr]
        df2 = df2.reset_index()
        db = pd.DataFrame({"BR": br_3})
        print(db)
        df2 = df2.join(db)
        print(df2)
        df2.to_csv("data/" + "aqp" + str(int(100 * Dr)) + ".csv",index=False)
    else:
        df3= df[df.Dr == Dr]
        df3 = df3.reset_index()
        db = pd.DataFrame({"BR": br_10})
        df3 = df3.join(db)
        print(df3)
        df3.to_csv("data/" + "aqp" + str(int(100 * Dr)) + ".csv",index=False)

save_one(0.1)
save_one(0.33)
save_one(1)