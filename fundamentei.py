from selenium import webdriver
import datetime
import time
import os

dict_empresas = {}


def pegaDados(empresa, driver):

    dict_empresa = {}

    try:
        driver.get("https://fundamentei.com/br/" + empresa)
    except:
        print("Não consegui acessar o site. " + empresa)
        return None

    # Nome da empresa, códigos das ações, resumo da empresa, setor(?)
    try:
        dict_empresa["Empresa"] = empresa

        dict_empresa["Empresa em uma linha"] = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[2]/div/div[1]/div[2]").text

        dict_empresa["Area de atuacao"] = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[2]/div/div[1]/div[3]/div/a").text

    except:
        print("Não consegui pegar o resumo da empresa. " + empresa)
        return None

    # Ranking de empresas do fundamentei
    try:
        avaliacao = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div/div[1]/div[1]").text

        temRanking = "ranking" in avaliacao

        if temRanking:
            dict_empresa["Rank Fundamentei"] = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/div/span").text
        else:
            dict_empresa["Rank Fundamentei"] = "-"

    except:
        print("Não consegui pegar o ranking " + empresa)
        return None

    # Governança, CEO, Segmento de listagem, tag along, free float, sócios..
    try:
        governanca = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]").text

        temCEO = "CEO" in governanca
        temSegmentoListagem = "SEGMENTO DE LISTAGEM" in governanca

        i = 2
        if temCEO:
            dict_empresa["CEO"] = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/span").text
        else:
            dict_empresa["CEO"] = "-"
            i = 1

        if temSegmentoListagem:
            dict_empresa["Segmento de Listagem"] = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div[" + str(i) + "]/div[1]/div/div").text
        else:
            dict_empresa["Segmento de Listagem"] = "-"

    except:
        print("Não consegui pegar a governança. " + empresa)
        return None

    # Market cap, n de empregados, % no ibov, data do balanco
    try:
        marketEmpregadosIbov = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[4]/div/div/div[1]").text

        temNumeroEmpregados = "N° de Empregados" in marketEmpregadosIbov
        temParticipacaoIbov = "Ibovespa" in marketEmpregadosIbov
        temMarketCap = "Market Cap" in marketEmpregadosIbov

        if temMarketCap:
            dict_empresa["Market Cap"] = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[3]/h1").text
        else:
            dict_empresa["Market Cap"] = "-"

        # if temNumeroEmpregados:
        #     dict_empresa["N° de Empregados"] = driver.find_element_by_xpath(
        #         "/html/body/div/div[2]/div[4]/div/div/div[1]/div[2]/div/div[3]/h1").text
        # else:
        #     dict_empresa["N° de Empregados"] = "-"

        # if temParticipacaoIbov:
        #     dict_empresa["Participacao no Ibovespa"] = driver.find_element_by_xpath(
        #         "/html/body/div/div[2]/div[4]/div/div/div[1]/div[3]/div/div[3]/h1").text
        # else:
        #     dict_empresa["Participacao no Ibovespa"] = "-"

    except:
        print("Não consegui pegar o market cap, nº empregados ou participacao no ibov " + empresa)
        return None

    # Tabela do balanco, só o corpo sem o cabecalho
    try:
        div = driver.find_element_by_xpath("/html/body/div/div[2]/div[5]").text
        temGraficoNoDiv = "Total de Ações" in div

        if temGraficoNoDiv:
            i = 3
        else:
            i = 2

        cabecalhoBalanco = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[5]/div[" + str(i) + "]/div[1]/table/thead").text
        balanco = driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[5]/div[" + str(i) + "]/div[1]/table/tbody").text

        temOpDescontinuada = "Op. Desc." in cabecalhoBalanco
        ehBanco = dict_empresa["Area de atuacao"] == "Bancos"

        cabecalhoTabelaGeralComOp = "Ano;Patrimonio Liquido;Receita Liquida;EBITDA;D&A;EBIT;Resultado Financeiro;Impostos;Operacao Descontinuada;Lucro Liquido;Margem Liquida;ROE;Caixa;Divida;Divida Liquida/EBITDA;FCO;CAPEX;FCF;FCL CAPEX;Proventos;Payout\n".upper()
        cabecalhoTabelaGeralSemOp = "Ano;Patrimonio Liquido;Receita Liquida;EBITDA;D&A;EBIT;Resultado Financeiro;Impostos;Lucro Liquido;Margem Liquida;ROE;Caixa;Divida;Divida Liquida/EBITDA;FCO;CAPEX;FCF;FCL CAPEX;Proventos;Payout\n".upper()
        cabecalhoTabelaBancos = "Ano;Patrimonio Liquido;Receita Interna Financeira;Lucro Liquido;Margem Liquida;ROE;Indice de Basileia;PDD;PDD/Lucro Liquido;Proventos;Payout\n".upper()

        if ehBanco:
            dict_empresa["Balancos"] = (
                cabecalhoTabelaBancos + balanco.replace(" ", ";")).split("\n")
        else:
            if temOpDescontinuada:
                dict_empresa["Balancos"] = (
                    cabecalhoTabelaGeralComOp + balanco.replace(" ", ";")).split("\n")
            else:
                dict_empresa["Balancos"] = (
                    cabecalhoTabelaGeralSemOp + balanco.replace(" ", ";")).split("\n")

    except:
        print("Não consegui pegar a tabela de balancos " + empresa)
        return None

    dict_empresas[empresa] = dict_empresa


def fundamenteiLogin():
    # Opcao para nao abrir o driver
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    # Loga no site com login e senha dados no arquivo.txt separados por quebra de linha ----> USAR CRIPTOGRAFIA(?)
    arqConta = open("conta.txt", "r")
    conta = arqConta.read()
    conta = conta.split("\n")

    # Liga o driver do chrome
    driver = webdriver.Chrome(
        executable_path='ChromeDriver/chromedriver.exe', options=option)

    # Entra na pagina e loga
    driver.get("https://fundamentei.com/login")

    emailXpath = "/html/body/div/div/div/div/div[2]/div[2]/form/input[1]"
    senhaXpath = "/html/body/div/div/div/div/div[2]/div[2]/form/input[2]"
    botaoXpath = "html/body/div/div/div/div/div[2]/div[2]/form/button"

    driver.find_element_by_xpath(
        emailXpath).send_keys(conta[0])
    driver.find_element_by_xpath(senhaXpath).send_keys(conta[1])
    driver.find_element_by_xpath(botaoXpath).click()

    # Tempo de delay pra logar no site
    time.sleep(1.5)
    return driver


def escreveArquivoCSV(data):
    avisoValores = "Os valores acima estão em BRL (reais) e na escala de milhões — 10.000 equivalem à 10 bilhões de reais. P na tabela significa Prejuízo."

    with open("Dados/dados_fundamentei_" + data + ".csv", "w", encoding="utf-8") as geral:

        # Escreve cabecalho do arquivo de dados. ITUB é a referência para esse cabecalho
        for i in dict_empresas["ITUB"]:
            if i != "Balancos":
                geral.write(i.upper() + ";")
        geral.write("\n")

        for empresa in dict_empresas:
            with open("Dados/" + empresa + "_balancos.csv", "w", encoding="utf-8") as f:

                # Escreve dados da empresa no arquivo de dados
                for chaveDado in dict_empresas[empresa]:
                    if chaveDado != "Balancos":
                        valorDado = (dict_empresas[empresa])[chaveDado]

                        # Se for uma lista para escrever no arquivo.. fazer isso:
                        if str(type(valorDado)) == "<class 'list'>":
                            info = ""
                            for elemento in valorDado:
                                info = info + str(elemento) + ","
                            info = info[:-1]
                            geral.write(info + ";")
                        else:
                            geral.write(valorDado + ";")
                geral.write("\n")

                # Escreve tabela no arquivo da empresa
                for linha_balanco in dict_empresas[empresa]["Balancos"]:
                    if "TTM" not in linha_balanco:
                        f.write(linha_balanco + "\n")
                f.write("\n" + avisoValores)


if __name__ == '__main__':
    # Inicia timer pra saber tempo de execucao do programa
    start = time.time()
    driver = fundamenteiLogin()

    # Data do dia
    d = datetime.datetime.today()
    dateFormated = d.strftime('%d_%m_%Y')

    # Abre os arquivos
    arqEntrada = open("empresas.txt", "r")

    # Le os códigos das empresas e faz uma lista
    empresas = arqEntrada.read()
    empresas = empresas.split("\n")

    for empresa in empresas:
        # Pega informacao empresa por empresa e coloca em um arquivo
        pegaDados(empresa, driver)

    # Escreve os dados pegos em 1 arquivo geral + 1 arquivo para cada empresa
    escreveArquivoCSV(dateFormated)

    # Fecha todos arquivos abertos e o driver
    arqEntrada.close()
    driver.quit()

    # Calcula tempo que o programa demora
    end = time.time()
    elapsed = end - start
    print("\n\nFundamentei executou em " + time.strftime("%H:%M:%S",
                                                         time.gmtime(elapsed)) + ". Dia: " + dateFormated + "\n\n")
