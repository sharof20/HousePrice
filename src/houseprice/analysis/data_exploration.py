# IMPORTING PACKAGES

import matplotlib.pyplot as plt  # visualization
import pandas as pd  # data processing
import seaborn as sb  # visualization

sb.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (20, 10)

# IMPORTING DATA

df = pd.read_csv("house.csv")
df.set_index("Id", inplace=True)

df.head(5)

# EDA

df.dropna(inplace=True)


df.describe()


df["MasVnrArea"] = pd.to_numeric(df["MasVnrArea"], errors="coerce")
df["MasVnrArea"] = df["MasVnrArea"].astype("int64")


# DATA VISUALIZATION

# 1. Heatmap

sb.heatmap(df.corr(), annot=True, cmap="magma")

plt.savefig("heatmap.png")
plt.show()

# 2. Scatter plot


def scatter_df(y_var):
    df.drop(y_var, axis=1)
    i = df.columns

    sb.scatterplot(i[0], y_var, data=df, color="orange", edgecolor="b", s=150)
    plt.title(f"{i[0]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[0]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter1.png")
    plt.show()

    sb.scatterplot(i[1], y_var, data=df, color="yellow", edgecolor="b", s=150)
    plt.title(f"{i[1]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[1]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter2.png")
    plt.show()

    sb.scatterplot(
        i[2],
        y_var,
        data=df,
        color="aquamarine",
        edgecolor="b",
        s=150,
    )
    plt.title(f"{i[2]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[2]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter3.png")
    plt.show()

    sb.scatterplot(
        i[3],
        y_var,
        data=df,
        color="deepskyblue",
        edgecolor="b",
        s=150,
    )
    plt.title(f"{i[3]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[3]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter4.png")
    plt.show()

    sb.scatterplot(
        i[4],
        y_var,
        data=df,
        color="crimson",
        edgecolor="white",
        s=150,
    )
    plt.title(f"{i[4]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[4]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter5.png")
    plt.show()

    sb.scatterplot(
        i[5],
        y_var,
        data=df,
        color="darkviolet",
        edgecolor="white",
        s=150,
    )
    plt.title(f"{i[5]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[5]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter6.png")
    plt.show()

    sb.scatterplot(i[6], y_var, data=df, color="khaki", edgecolor="b", s=150)
    plt.title(f"{i[6]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[6]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter7.png")
    plt.show()

    sb.scatterplot(i[7], y_var, data=df, color="gold", edgecolor="b", s=150)
    plt.title(f"{i[7]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[7]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter8.png")
    plt.show()

    sb.scatterplot(i[8], y_var, data=df, color="r", edgecolor="b", s=150)
    plt.title(f"{i[8]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[8]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter9.png")
    plt.show()

    sb.scatterplot(
        i[9],
        y_var,
        data=df,
        color="deeppink",
        edgecolor="b",
        s=150,
    )
    plt.title(f"{i[9]} / Sale Price", fontsize=16)
    plt.xlabel(f"{i[9]}", fontsize=14)
    plt.ylabel("Sale Price", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig("scatter10.png")
    plt.show()


scatter_df("SalePrice")

# 3. Distribution plot

sb.distplot(df["SalePrice"], color="r")
plt.title("Sale Price Distribution", fontsize=16)
plt.xlabel("Sale Price", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("distplot.png")
plt.show()
