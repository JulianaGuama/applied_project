# Projeto Aplicado
Projeto Aplicado IGTI para MBA de Machine Learning.

# Setup
Para reproduzir este experimento, siga os passos:
* prepare o seu ambiente garantindo que o `requirements.txt` seja instalado: `pip install -r requirements.txt`
* rode o arquivo `explore.py` que irá gerar o file `books.csv`
* faça [upload do 'books.csv'](https://docs.databricks.com/data/data.html) no databricks
* faça o [upload do 'MBA projeto aplicado.ipynb'](https://docs.databricks.com/data/data.html) no databricks
* Substitua o cmd6 `df = spark.read.format("csv").option("delimiter", ";").option("header", True).load("dbfs:/FileStore/shared_uploads/juliana.guama@gmail.com/books-1.csv")` pela importação de arquivo sugerida pela API do databricks quando você subiu o `books.csv`.



