from load_file import read_files


if __name__ == "__main__":
    root_file = "Brazilian_Portugese_Corpus/"
    files = read_files(root_file)
    print(files.keys())
    root_key = root_file.replace("/", "")
    print(type(files[root_key]))
    for author in files[root_key].keys():
        print("Author: ", author)
        print("Amount books: ", len(files[root_key][author].keys()) )

        for title, book in files[root_key][author].items():
            print("Title: ", title)
            print("Book size: ", len(book))

