Para utilizar o assistente, primeiro instale os pacotes necessários utilizando o comando `pip install -r requirements.txt`. Em seguida monte o arquivo executável usando o pyinstaller: `pyinstaller build.spec`.

> :warning: Atenção!
> Você deve criar um arquivo `.env` na raíz do projeto com o seguinte formato:
>
> ```
> CLIENT_ID="<client_id>"
> CLIENT_SECRET="<client_secret>"
> ```

Por fim, você pode executar o aplicativo encontrado em `./dist/Guess The Song.exe`
