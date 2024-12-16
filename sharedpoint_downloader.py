import os
import requests

# Configurações de autenticação - Substitua os valores abaixo conforme necessário
tenant_id = "<Tenant-ID>"  # ID do Tenant no Azure Active Directory
client_id = "<Client-ID>"  # ID do Aplicativo registrado no Azure AD
client_secret = "<Client-Secret>"  # Secret gerado no Certificates & Secrets
scope = "https://graph.microsoft.com/.default"

# URL para obter o token de autenticação
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": scope,
}

# Solicitar token OAuth
response = requests.post(token_url, data=data)
token = response.json().get("access_token")

# Função para download recursivo de arquivos
def download(drive_id, folder_path, local_path, headers):
    folder_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children"
    folder_response = requests.get(folder_url, headers=headers)

    if folder_response.status_code == 200:
        items = folder_response.json().get('value', [])
        if not items:
            print(f"Nenhum item encontrado na pasta: {folder_path}")
        else:
            # Cria a pasta local, se não existir
            os.makedirs(local_path, exist_ok=True)

            for item in items:
                item_name = item['name']
                print(f"Encontrado: {item_name}")

                # Se for uma pasta, chama a função novamente (recursividade)
                if item.get('folder'):
                    new_folder_path = f"{folder_path}/{item_name}"
                    new_local_path = os.path.join(local_path, item_name)
                    download(drive_id, new_folder_path, new_local_path, headers)
                # Se for um arquivo, realiza o download
                elif '@microsoft.graph.downloadUrl' in item:
                    download_url = item['@microsoft.graph.downloadUrl']
                    file_path = os.path.join(local_path, item_name)
                    file_content = requests.get(download_url).content
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                    print(f"Arquivo baixado: {file_path}")
    else:
        print(f"Erro ao acessar a pasta: {folder_response.status_code}")
        print(folder_response.text)

# Execução principal
if token:
    print("Token obtido com sucesso!")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    # Substitua pelo domínio e nome do site SharePoint
    site_url = "https://graph.microsoft.com/v1.0/sites/<site-domain>:/sites/<site-name>"
    site_response = requests.get(site_url, headers=headers)

    if site_response.status_code == 200:
        site_info = site_response.json()
        site_id = site_info['id']
        print(f"Site ID: {site_id}")

        # Obtém as bibliotecas de documentos do site
        drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives_response = requests.get(drives_url, headers=headers)

        if drives_response.status_code == 200:
            drives = drives_response.json().get('value', [])
            drive_id = None

            # Encontre o drive correto pelo nome (normalmente "Documentos")
            for drive in drives:
                print(f"Drive encontrado: {drive['name']} (ID: {drive['id']})")
                if drive['name'] == "Documentos":  # Alterar se necessário
                    drive_id = drive['id']
                    break

            if drive_id:
                # Caminho da pasta no SharePoint (a partir da biblioteca Documentos)
                folder_path = "<folder-path>"  # Ex: "Pasta/Subpasta" ou "" para a raiz

                # Caminho local onde os arquivos serão salvos
                local_path = r"C:\caminho\local"  # Ex: r"C:\backup" ou compartilhamento UNC

                # Baixa arquivos e pastas
                download(drive_id, folder_path, local_path, headers)
            else:
                print("Biblioteca 'Documentos' não encontrada.")
        else:
            print(f"Erro ao obter drives: {drives_response.status_code}")
            print(drives_response.text)
    else:
        print(f"Erro ao obter informações do site: {site_response.status_code}")
        print(site_response.text)
else:
    print("Falha ao obter token.")
