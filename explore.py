import json
import pandas as pd
from load_file import read_files



if __name__ == "__main__":
    root_file = "Brazilian_Portugese_Corpus/"
    files = read_files(root_file)
    root_key = root_file.replace("/", "")

    with open("./books.json", "w", encoding='utf8') as f:
        json.dump(files[root_key], f, ensure_ascii=False)

    df = pd.DataFrame(columns=["author", "title", "book"])

    row = list()

    for author in files[root_key].keys():
        print("\n\nAuthor: ", author)
        print("Amount books: ", len(files[root_key][author].keys()) )

        for title, book in files[root_key][author].items():
            str_book = book.replace("\n", " ")
            row = [author, title, str_book]
            df.loc[len(df)] = row
            #print("Title: ", title)
            #print("Book size: ", len(book))

    print(df.head())
    df.to_csv("./books.csv", sep=";", encoding="utf8")
    print("saved")