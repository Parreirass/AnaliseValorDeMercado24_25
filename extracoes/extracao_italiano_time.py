# JOGADORES PREMIER LEAGUE 24/25 (CAMPEONATO COMPLETO)
import time
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================
# CONFIGURAÇÕES
# ==============================================
URL = "https://www.sofascore.com/pt/torneio/futebol/italy/serie-a/23#id:63515,tab:statistics"
OUTPUT_ARQUIVO = "sofascore_italiano_geral_final_valor_de_mercado_24_25.csv"
TEMPO_ESPERA = 20

chrome_options = Options()
# chrome_options.add_argument("--headless=new") # Descomente para rodar sem interface gráfica (RECOMENDADO para grandes volumes)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(URL)
    wait = WebDriverWait(driver, TEMPO_ESPERA)
    print("✅ Navegador iniciado e página carregada.")
except Exception as e:
    raise SystemExit(f"❌ Erro ao iniciar o navegador: {e}")

# ==============================================
# FUNÇÕES AUXILIARES
# ==============================================
def extrair_tabela(driver_instance):
    """Extrai os dados da tabela visível e retorna um DataFrame."""
    try:
        # Tenta extrair a tabela do elemento com id="tabpanel-summary"
        table_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tabpanel-summary"]/div/table'))
        )
        tabela_html = table_element.get_attribute("outerHTML")
        # pd.read_html é robusto para ler o HTML da tabela
        df = pd.read_html(StringIO(tabela_html))[0]
        # Remove colunas sem nome
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        print(f"⚠️ Erro ao extrair a tabela: {e}")
        return None

def extrair_dados_jogador(driver_instance, url_jogador):
    """
    Acessa a página individual do jogador (em uma nova aba) e extrai as informações necessárias.
    """
    # [NOVO] Adicionado 'Time' ao dicionário
    dados = {
        'Valor de mercado': None,
        'Pontos fortes': None,
        'Pontos fracos': None,
        'Posição': None,
        'Idade': None,
        'Time': None
    }
    original_window = driver_instance.current_window_handle
    
    try:
        # 1. Abre uma nova aba e muda o foco
        driver_instance.execute_script("window.open('');")
        driver_instance.switch_to.window(driver_instance.window_handles[-1])
        
        # 2. Navega para a URL do jogador
        driver_instance.get(url_jogador)
        wait_tab = WebDriverWait(driver_instance, 10)
        
        # 3. Extrai o valor de mercado
        try:
            valor_elem = wait_tab.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'Box') and .//div[text()='Valor de mercado']]//div[contains(@class, 'Text') and contains(@color, 'sofaSingles.value')]")
                )
            )
            dados['Valor de mercado'] = valor_elem.text
        except:
            print(f"⚠️ Valor de mercado não encontrado para {url_jogador}")

        # 4. Extrai os pontos fortes
        try:
            # Encontra todos os spans de dados (c_neutrals.nLv1) DENTRO do container que tem o TÍTULO "Pontos fortes"
            spans_fortes = driver_instance.find_elements(
                By.XPATH,
                "//div[contains(@class, 'pb_xl') and .//span[text()='Pontos fortes']]//span[contains(@class, 'c_neutrals.nLv1')]"
            )
            if spans_fortes:
                dados['Pontos fortes'] = '; '.join([span.text for span in spans_fortes])
        except:
            print(f"⚠️ Pontos fortes não encontrados para {url_jogador}")

        # 5. Extrai os pontos fracos
        try:
            # Encontra todos os spans de dados (c_neutrals.nLv1) DENTRO do container que tem o TÍTULO "Pontos fracos"
            spans_fracos = driver_instance.find_elements(
                By.XPATH,
                "//div[contains(@class, 'pb_xl') and .//span[text()='Pontos fracos']]//span[contains(@class, 'c_neutrals.nLv1')]"
            )
            if spans_fracos:
                # Usa join para o caso de haver múltiplos pontos fracos, ou apenas um (como "Sem pontos fracos...")
                dados['Pontos fracos'] = '; '.join([span.text for span in spans_fracos])
        except:
            print(f"⚠️ Pontos fracos não encontrados para {url_jogador}")

        # 6. Extrai Idade (div[2]) e Posição (div[3])
        try:
            # Esta classe localiza vários elementos: 1º (País), 2º (Idade), 3º (Posição)
            elementos_info = driver_instance.find_elements(
                By.XPATH,
                "//div[contains(@class, 'd_flex ai_center gap_xs px_sm first:ps_0 last:pe_0')]"
            )
            
            # Extrai Idade (segundo elemento, índice 1)
            if len(elementos_info) >= 2:
                dados['Idade'] = elementos_info[1].text
            else:
                 print(f"⚠️ Idade não encontrada para {url_jogador}")

            # Extrai Posição (terceiro elemento, índice 2)
            if len(elementos_info) >= 3:
                dados['Posição'] = elementos_info[2].text
            else:
                print(f"⚠️ Posição não encontrada para {url_jogador}")
                
        except Exception as e:
            print(f"⚠️ Erro ao extrair Idade/Posição para {url_jogador}: {e}")
        
        # ===================================================================
        # 7. [NOVO] Extrai o Time
        # ===================================================================
        try:
            # Localiza o span com o nome do time dentro da div específica
            time_elem = wait_tab.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'd_flex flex-d_column jc_center gap_2xs')]/span[contains(@class, 'textStyle_body.medium')]")
                )
            )
            dados['Time'] = time_elem.text
        except:
            print(f"⚠️ Time não encontrado para {url_jogador}")
        # ===================================================================

    except TimeoutException:
        print(f"⚠️ Tempo esgotado para carregar {url_jogador}")
    except Exception as e:
        print(f"⚠️ Erro ao extrair dados de {url_jogador}: {e}")
    finally:
        # 8. Fecha a aba e retorna para a aba original
        try:
            driver_instance.close()
            driver_instance.switch_to.window(original_window)
        except WebDriverException as we:
            print(f"⚠️ Erro ao fechar/trocar de aba: {we}")
            pass
        return dados

def extrair_links_jogadores(driver_instance):
    """
    Extrai os links (href) dos jogadores da tabela visível.
    CORREÇÃO: Alterado o localizador de div#tabpanel-summary tbody/tr/td[3]//a
    para o XPATH correto: //div[@id='tabpanel-summary']//tbody/tr/td[3]//a
    """
    try:
        # Espera o carregamento da tabela
        WebDriverWait(driver_instance, TEMPO_ESPERA).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#tabpanel-summary table"))
        )
        
        links_jogadores = []
        # Localiza todos os links 'a' dentro da terceira coluna da tabela de estatísticas (onde está o nome do jogador)
        # Este é o XPath corrigido
        link_elements = driver_instance.find_elements(By.XPATH, "//div[@id='tabpanel-summary']//tbody/tr/td[3]//a")
        
        for link in link_elements:
            href = link.get_attribute("href")
            # Garante que o link seja completo
            if href and not href.startswith("http"):
                href = "https://www.sofascore.com" + href
            links_jogadores.append(href)
            
        return links_jogadores
    except Exception as e:
        print(f"⚠️ Erro ao extrair links dos jogadores: {e}")
        return []

def extrair_dados_completos_da_pagina(driver_instance, wait_instance, pagina_numero):
    """Extrai a tabela, os links e os valores de mercado para uma única página."""
    print(f"  - 1/3: Extraindo tabela da página {pagina_numero}...")
    df = extrair_tabela(driver_instance)
    
    if df is None or df.empty:
        print("  - ❌ Tabela vazia. Pulando.")
        return None
    
    print(f"  - 2/3: Extraindo links dos jogadores (total de {len(df)})...")
    links_jogadores = extrair_links_jogadores(driver_instance)
    
    if len(links_jogadores) != len(df):
        print(f"  - ⚠️ Aviso: Número de links ({len(links_jogadores)}) diferente do número de linhas ({len(df)}). Corrigindo lista de links.")
        # Adiciona Nones se links faltarem, para evitar erro no zip
        while len(links_jogadores) < len(df):
                links_jogadores.append(None)
        links_jogadores = links_jogadores[:len(df)]
    
    df["Link Jogador"] = links_jogadores
    
    print("  - 3/3: Extraindo dados completos dos jogadores...")
    dados_jogadores = []
    
    # Itera sobre o DataFrame para extrair os dados
    for index, row in df.iterrows():
        url_jogador = row["Link Jogador"]
        nome_jogador = row.get("Nome", "Nome não disponível")
        
        print(f"\n{'='*70}")
        print(f"Jogador #{index + 1}: {nome_jogador}")
        print(f"{'='*70}")
        
        print("\n📊 ESTATÍSTICAS (da tabela principal):")
        # [MODIFICADO] Removido o print do "Time" daqui
        print(f"⚽ Gols: {row.get('Gols', 'N/A')}")
        print(f"📈 Gols esperados (xG): {row.get('Gols esperados (xG)', 'N/A')}")
        print(f"🎯 Dribles certos: {row.get('Dribles certos', 'N/A')}")
        print(f"🛡️ Desarmes: {row.get('Desarmes', 'N/A')}")
        print(f"🎯 Assistências: {row.get('Assistências', 'N/A')}")
        print(f"📊 Acerto no passe %: {row.get('Acerto no passe %', 'N/A')}")
        print(f"⭐ Média Sofascore: {row.get('Média das notas Sofascore', 'N/A')}")
        
        if url_jogador and pd.notna(url_jogador):
            dados = extrair_dados_jogador(driver_instance, url_jogador)
            dados_jogadores.append(dados)
            
            print("\n📝 INFORMAÇÕES ADICIONAIS (da pág. individual):")
            # [NOVO] Adicionado print do "Time" extraído da pág. individual
            print(f"🏃 Time: {dados['Time'] or 'Não encontrado'}")
            print(f"💰 Valor de mercado: {dados['Valor de mercado'] or 'Não encontrado'}")
            print(f"🎂 Idade: {dados['Idade'] or 'Não encontrada'}")
            print(f"💪 Pontos fortes: {dados['Pontos fortes'] or 'Não encontrados'}")
            print(f"⚠️ Pontos fracos: {dados['Pontos fracos'] or 'Não encontrados'}")
            print(f"🎯 Posição: {dados['Posição'] or 'Não encontrada'}")
        else:
            print("\n❌ Link do jogador não disponível")
            # [NOVO] Adicionado 'Time': None
            dados_jogadores.append({
                'Valor de mercado': None,
                'Pontos fortes': None,
                'Pontos fracos': None,
                'Posição': None,
                'Idade': None,
                'Time': None
            })
            
        print(f"{'='*70}")
    
    # [NOVO] Adicionado 'Time' ao loop
    # Isso irá SOBRESCREVER a coluna 'Time' que veio da tabela principal
    # com os dados mais precisos da página individual.
    colunas_para_adicionar = ['Valor de mercado', 'Pontos fortes', 'Pontos fracos', 'Posição', 'Idade', 'Time']
    for coluna in colunas_para_adicionar:
        # Se a coluna (ex: 'Time') já existir, ela será sobrescrita.
        # Se não existir (ex: 'Idade'), ela será criada.
        df[coluna] = [dados[coluna] for dados in dados_jogadores]
        
    print(f"  - ✅ Dados da página {pagina_numero} processados com sucesso.")
    return df

# ==============================================
# ETAPAS DE SCRAPING
# ==============================================
dfs = [] # Lista para armazenar DataFrames de cada página

try:
    # 1️⃣ Aceita cookies
    try:
        print("⏳ Procurando banner de cookies...")
        cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[p[text()='Aceitar tudo']]")))
        cookie_button.click()
        print("✅ Banner de cookies aceito.")
        time.sleep(1) # Espera a página se estabilizar
    except TimeoutException:
        print("✔️ Banner de cookies não encontrado.")

    # 2️⃣ Clica na aba "Estatísticas"
    try:
        print("⏳ Clicando na aba principal 'Estatísticas'...")
        stats_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='tablist']//button[contains(., 'Estatísticas')]")))
        stats_tab.click()
        print("✅ Aba 'Estatísticas' selecionada.")
    except TimeoutException:
        raise SystemExit("❌ A aba principal 'Estatísticas' não foi encontrada.")

    # 3️⃣ Clica na sub-aba "Geral"
    try:
        print("⏳ Clicando na sub-aba 'Geral'...")
        # Localiza a sub-aba "Geral" dentro do contêiner de sub-abas
        geral_tab_locator = (By.XPATH, "//div[@role='tablist']//button[@data-testid='tab-summary']")
        geral_tab = wait.until(EC.element_to_be_clickable(geral_tab_locator))
        geral_tab.click()
        print("✅ Sub-aba 'Geral' selecionada.")
        time.sleep(1) # Espera o conteúdo da aba carregar
    except TimeoutException:
        raise SystemExit("❌ A sub-aba 'Geral' não foi encontrada.")

    # ===================================================================
    # 3.5️⃣ CLICA NO RADIO BUTTON "JOGADORES COM MENOS JOGOS"
    # ===================================================================
    try:
        print("⏳ Procurando o radio button 'Jogadores com menos jogos'...")
        
        # XPath atualizado para ser mais robusto, baseado no texto da label
        # Ele localiza a label pelo texto e clica no input associado a ela
        radio_button_locator = (
            By.XPATH, 
            "//label[.//span[text()='Jogadores com menos jogos']]/input"
        )
        
        # Espera o elemento ser clicável
        radio_button = wait.until(EC.element_to_be_clickable(radio_button_locator))
        
        # Usa JavaScript para clicar, é mais confiável para inputs customizados
        driver.execute_script("arguments[0].click();", radio_button)
        
        print("✅ Radio button 'Jogadores com menos jogos' clicado.")
        
        # ESPERA CRÍTICA: A tabela precisa recarregar com os dados filtrados
        # Sem isso, o script extrairá os dados antigos (não filtrados)
        print("⏳ Aguardando a tabela ser atualizada com os filtros...")
        time.sleep(3) 
        
    except TimeoutException:
        print("⚠️ O radio button 'Jogadores com menos jogos' não foi encontrado ou não era clicável.")
    except Exception as e:
        print(f"⚠️ Erro ao clicar no radio button 'Jogadores com menos jogos': {e}")
    # ===================================================================

    # 4️⃣ Loop de extração e paginação
    pagina_atual = 1
    
    while True:
        if pagina_atual > 35:
            print("✅ Limite de 35 páginas atingido. Encerrando extração.")
            break
        
        print(f"\n==============================================")
        # Formato de impressão ligeiramente ajustado para centralizar
        print(f"| INICIANDO EXTRAÇÃO DA PÁGINA {pagina_atual}{' ' if pagina_atual < 10 else ''}|") 
        print(f"==============================================")
        
        df_pagina = extrair_dados_completos_da_pagina(driver, wait, pagina_atual)
        
        if df_pagina is not None:
            dfs.append(df_pagina)
        else:
            # Se a extração falhou ou a tabela estava vazia, para o loop
            print("🚫 Falha na extração ou tabela vazia. Terminando o loop de paginação.")
            break

        # Tenta encontrar e clicar no botão "próximo"
        try:
            # Localiza o botão "próximo" com o SVG e path exatos e sem atributo disabled
            paginacao_div = driver.find_element(By.XPATH, "//div[contains(@class, 'd_flex ai_center jc_center py_lg')]")
            # print(paginacao_div.get_attribute("outerHTML"))
            botoes_html = []
            botoes = driver.find_elements(By.XPATH, "//button[contains(@class, 'button button--variant_clear button--size_primary button--colorPalette_primary button--negative_false px_0 br_xs')]")
            #print(paginacao_div2.get_attribute("outerHTML"))

            # for botao in botoes:
            #     html = botao.get_attribute("outerHTML")
            #     botoes_html.append(html)
            #     print(html)

            next_buttons = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'd_flex ai_center jc_center py_lg')]"
                "//button[not(@disabled) and .//svg[contains(@class, 'SvgWrapper fyGiev')]/path[@d='M18 12.01 9.942 20 8.51 18.58l6.636-6.57L8.5 5.41 9.922 4z']]"
            )
            # next_button_locator = (
            #     By.XPATH,
            #     "//button[.//path[contains(@d, 'M18 12.01')] and not(@disabled)]"
            # )
            # next_button = driver.find_element(*next_button_locator)
            # print("✅ Botão 'próximo' encontrado com sucesso!")
            print("Botões encontrados:", next_buttons)
            print(f"Botões próximos encontrados: {len(next_buttons)}")
            if len(botoes) > 1 and botoes[1].is_displayed() and botoes[1].is_enabled():
                driver.execute_script("arguments[0].click();", botoes[1])
                print("➡️ Clique enviado para ir para a próxima página (botoes[1])...")
                time.sleep(2)
                pagina_atual += 1
            else:
                print("🚫 Botão 'próximo' não encontrado ou está desabilitado. Fim da paginação.")
                break
            # Define o localizador para o botão "próximo" que NÃO está desabilitado
            # next_button_locator = (
            #     By.XPATH,
            #     "//button[.//path[contains(@d, 'M18 12.01')] and not(@disabled)]"
            # )

            # # O Selenium tentará encontrar o elemento. Se não encontrar, pulará para o bloco 'except'.
            # next_button = driver.find_element(*next_button_locator)
            
            # print("✅ Botão 'próximo' encontrado com sucesso!")
            # # Aqui você realizaria a ação, por exemplo:
            # next_button.click()

        except (NoSuchElementException, IndexError):
            print("✅ Fim da paginação. Botão 'próximo' não encontrado.")
            break
        except Exception as e:
            # Captura exceções como StaleElementReferenceException (raro aqui, mas possível)
            print(f"✅ Fim da paginação. Todas as páginas foram extraídas. Motivo: {e}")
            break

except WebDriverException as e:
    print(f"\n❌ ERRO CRÍTICO DO WEBDRIVER: {e}")
except Exception as e:
    print(f"\n❌ ERRO INESPERADO: {e}")

finally:
    # Garante que o navegador seja fechado, mesmo se houver erro
    driver.quit()
    
    if dfs:
        print("\n🔄 Processando e consolidando dados coletados...")
        df_final = pd.concat(dfs, ignore_index=True)

        # A coluna "Time" já está na lista, e como ela foi sobrescrita
        # durante a extração, ela terá o valor correto (da pág. individual).
        colunas_ordenadas = [
            "Link Jogador",
            "Time",
            "Jogador",
            "Valor de mercado",
            "Idade",
            "Pontos fortes",
            "Pontos fracos",
            "Posição",
            "Gols",
            "Gols esperados (xG)",
            "Dribles certos",
            "Desarmes",
            "Assistências",
            "Acerto no passe %",
            "Média das notas Sofascore"
        ]
        
        # Mantém apenas as colunas que existem no DataFrame
        colunas_existentes = [col for col in colunas_ordenadas if col in df_final.columns]
        # Adiciona quaisquer colunas que existam no DataFrame mas não estão na lista ordenada
        colunas_extras = [col for col in df_final.columns if col not in colunas_ordenadas]
        
        # Reorganiza as colunas
        df_final = df_final[colunas_existentes + colunas_extras]

        df_final.to_csv(OUTPUT_ARQUIVO, index=False, encoding="utf-8-sig")
        print(f"\n✅ Extração concluída! {len(df_final)} registros salvos em '{OUTPUT_ARQUIVO}'")
    else:
        print("\n⚠️ Nenhuma tabela foi extraída.")