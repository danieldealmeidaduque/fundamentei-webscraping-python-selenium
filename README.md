# FundamenteiWebScrap
Aplicação para pegar as informações das ações no site "Fundamentei"

-- Versão 0 - 01/08/2021

Quais empresas vou pegar no webscrapping?
  - O arquivo 'empresas.txt' tem o código de todas empresas do ibov separados por quebra de linha
  - Esse arquivo é usado como padrão na execução do código
  - Caso queira restringir a quantidade de ações, é só modificar esse arquivo para as ações que você quiser
  
Antes de executar
  - Verificar se existe a pasta "Dados" no mesmo diretório do arquivo "fundamentei.py", pois é nele que fica os arquivos de saída.
  - Precisa ter conta no fundamentei.com e colocar no arquivo "conta.txt"
    - Primeira linha somente o email
    - Segunda linha somente a senha
  - Verificar versão do chrome:
    - Clicar nos três pontos no canto superior direito do navegador > ajuda > sobre o google chrome
  - Baixar o chrome driver compatível com a versão do seu google chrome:
    - https://chromedriver.chromium.org/downloads
    - Colocar o chromedriver.exe baixado na pasta "ChromeDriver"

Como executar?
  - Abrir o arquivo em uma framework
  - Executar o arquivo 'fundamentei.py'
