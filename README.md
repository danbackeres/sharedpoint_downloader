# Instruções para alterar o arquivo

## Configurações de Autenticação
* Substituir `<Tenant-ID>`, `<Client-ID>`, `<Client-Secret>`

```python
tenant_id = "<Tenant-ID>"
client_id = "<Client-ID>"
client_secret = "<Client-Secret>"
```

## URL do Site SharePoint
* Substituir `<site-domain>` e `<site-name>` pelo domínio e nome do site.
* Exemplo: techbacker.sharepoint.com:/sites/Projetos.

```python
site_url = "https://graph.microsoft.com/v1.0/sites/<site-domain>:/sites/<site-name>"
```

## Nome da Biblioteca
* Normalmente, o nome é "Documentos", mas se for diferente, altere o código.
```python
if drive['name'] == "Documentos":
```

## Caminho da Pasta no SharePoint
* Especificar o caminho da pasta dentro da biblioteca.
* Exemplo: `Pasta/Subpasta` ou `""` para a raiz.
```python
folder_path = "<folder-path>"  # Ex: "Pasta/Subpasta"
```

## Caminho Local
* Caminho onde os arquivos serão salvos no computador ou no serrvidor.
* Pode ser uma pasta local (`C:backup`) ou um compartilhamento de rede (`\\servidor\pasta`).
```python
local_path = r"C:\caminho\local"  # Ex: r"\\servidor\pasta"
```

# Instruções para rodar o código

## Pré-requisitos
* Python 3.8 + instalado.
* Biblioteca *requests* instalada.
```python
pip install requests
```

## Passos para Rodar o Código

1. Clone o repositório ou baixe o arquivo `backup_sharepoint.py`
2. Configure as variáveis no script:
    * Abra o arquivo `backup_sharepoint.py` em um editor de texto.
    * Substitua os valores de `<Tenant-ID>`, `<Client-ID>`, `<Client-Secret>`, `<site-domain>`, `<site-name>`, `<folder-path>` e `<local-path>` conforme necessário.
3. python backup_sharepoint.py
    ```python 
    python backup_sharepoint.py
    ```
4. Verifique os arquivos baixados no diretório especificado em `local_path`.
