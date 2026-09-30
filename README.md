
# Análise de Desempenho e Valuation nas Quatro Principais Ligas Europeias: Uma Abordagem de Data Science (Temporada 24/25)

Felipe Parreiras Dias

Engenharia de Computação / CEFET-MG

5 de dezembro de 2025

## 1 Introdução

O futebol moderno transcendeu as quatro linhas, consolidando-se como uma indústria bilionária onde a tomada de decisão baseada em dados (Data Analytics) tornou-se um diferencial competitivo crucial. Clubes eu- ropeus investem massivamente na contratação de atletas, muitas vezes baseando-se em avaliações subjetivas que po- dem levar a ineficiências financeiras.

Este projeto insere-se no contexto do Football Analytics, investigando a relação entre o desempenho técnico indivi- dual e o valor de mercado dos jogadores nas quatro prin- cipais ligas da Europa: Bundesliga (Alemanha), Premier League (Inglaterra), La Liga (Espanha) e Serie A (Itália). A motivação do estudo reside na necessidade de demo- cratizar ferramentas de scouting e valuation, permitindo identificar talentos subvalorizados e otimizar orçamentos.

A abordagem adotada combina técnicas de estatísticas individuais de jogadores, visualização de dados e apren- dizado de máquina supervisionado para criar um modelo de análise comparativa, tanto intra-ligas quanto em um cenário global europeu.

## 2 Descrição do Problema

O fenômeno analisado é a precificação de ativos esportivos (jogadores) e sua correlação com a performance real em campo. Observa-se no mercado atual uma disparidade significativa de valores, onde a liga de origem muitas vezes inflaciona o preço de um atleta independentemente de suas estatísticas.

O escopo da pesquisa limita-se à temporada 2024/2025, focando nos jogadores ativos nas primeiras divisões da Ale- manha, Inglaterra, Espanha e Itália. A escolha destas ligas justifica-se por concentrarem o maior volume financeiro e os dados mais robustos do futebol mundial.

Um dos principais desafios encontrados, e abordados neste trabalho, é a inconsistência e a volatilidade dos da- dos: transferências ocorrem durante a temporada (joga- dores mudando de liga), e as nomenclaturas de clubes va- riam entre bases de dados (ex: "Man Utd"em tabelas ofici- ais versus "Manchester United"em bases estatísticas), exi- gindo um tratamento rigoroso de integridade referencial. Além disso, as características individuais de cada jogador se misturam com suas estatísticas em campo no momento

de sua precificação, o que deve ser analisado com cuidado para identificar os aspectos que mais contribuem para o aumento do valor de mercado.

## 3 Objetivos do Trabalho

## 3.1 Objetivo Geral

Desenvolver uma estrutura analítica de dados capaz de comparar o desempenho e o valor de mercado de jogado- res europeus, identificando ineficiências de precificação e oportunidades de contratação.

## 3.2 Objetivos Específicos

- Coletar e tratar dados de jogadores e classificações das quatro ligas, solucionando inconsistências de no- menclatura.

- Desenvolver métricas de eficiência coletiva (Custo por Ponto) e individual (Índice Atlas).

- Aplicar algoritmos de Regressão Linear e Random Forrest para estimar o "Valor Justo"e classificar jo- gadores como super ou subvalorizados.

- Comparar o perfil econômico e tático entre as ligas.

- Criar uma ferramenta interativa de scouting para fil- tragem de jogadores por atributos específicos.

## 4 Metodologia

## 4.1 Ferramentas Utilizadas

O projeto foi desenvolvido em linguagem Python, utili- zando o ambiente Jupyter Notebook para prototipagem rápida e análise exploratória. As principais bibliotecas fo- ram:

- Selenium: Extração dos dados na web de forma au- tomática.

- Pandas: Manipulação e estruturação dos dados ta- bulares.

- NumPy: Operações numéricas e vetoriais.


- Scikit-learn: Implementação do modelo de Regres- são Linear.

- Plotly Express e Seaborn: Visualização de dados interativa e estática.

## 4.2 Extração dos Dados

Os dados foram obtidos através de datasets em formato CSV provenientes da plataforma SofaScore. Foram uti- lizados oito arquivos no total: quatro contendo estatísticas individuais detalhadas (valor, idade, notas, gols) e quatro contendo as tabelas de classificação (standings) oficiais de cada campeonato. Para a extração dos dataset´s com os jogadores de cada campeonato, foi utilizada a biblioteca Selenium, preferida por fazer a extração de forma auto- mática e navegação dentro do navegador de forma estra- tégica.

## 4.3 Tratamento e Preparação dos Dados

Uma etapa que demandou muita atenção durante a cons- trução do projeto. Os dados brutos apresentavam natu- reza heterogênea, ou seja, não são uniformes, exigindo:

- 1. Limpeza de Variáveis Numéricas: Conversão de valores monetários (ex: "€124M"para 1.24 × 108) e tratamento de strings de idade ("3 de maio de 2004 (21)"para "21").

- 2. Correção de Nomes de Times: Criação de dicio- nários (Hash Maps) para padronizar nomes de equi- pes entre os arquivos de jogadores e tabelas (ex: ma- pear "Leverkusen"para "Bayer 04 Leverkusen").

- 3. Gestão de Transferências: Implementação de um algoritmo de correção para realocar jogadores trans- feridos (como Florian Wirtz ou Matthijs de Ligt) aos seus times de origem na temporada 24/25, garantindo a consistência das estatísticas.

- 4. Tratamento de Missing Values: Preenchimento de nulos com zero em estatísticas de jogo e remoção de registros inconsistentes.

## 4.4 Visualização dos Dados

Para a análise visual, utilizou-se Seaborn para matrizes de correlação e boxplots, e Plotly para gráficos de disper- são interativos.

- Scatter Plots: Escolhidos para relacionar duas va- riáveis contínuas (ex: Valor vs. Pontos), permitindo identificar outliers visuais.

- Boxplots: Utilizados para comparar a distribuição de preços entre as ligas, evidenciando a mediana e a dispersão (inflação).

- Gráficos de barras: Aplicados para visualizar as diferenças entre as ligas, no que diz respeito às suas características gerais (gols, assistências, média de no- tas, etc.).

## 4.5 Modelagem e Machine Learning

Nesta etapa, aplicaram-se técnicas de Aprendizado de Má- quina Supervisionado para realizar o valuation (precifica- ção justa) dos atletas. O experimento foi conduzido em duas fases: uma modelagem inicial utilizando Regressão Linear e uma modelagem avançada utilizando Random Forest Regressor.

A estrutura dos dados para o treinamento foi definida da seguinte forma:

- Variável Alvo (Y): Valor de Mercado (numérico).

- Features (X): Variáveis numéricas (Idade, Gols, As- sistências, Dribles, Nota SofaScore) e variáveis cate- góricas (Posição e Liga), estas últimas tratadas via técnica de One-Hot Encoding.

A escolha pela transição da Regressão Linear para o Random Forest justificou-se por limitações teóricas do pri- meiro modelo frente à natureza dos dados. Enquanto a regressão linear pressupõe uma relação constante entre as variáveis, o mercado do futebol apresenta comportamentos não-lineares complexos, especificamente:

- 1. A Curva da Idade: A desvalorização de um atleta não é linear; ela tende a ser estável durante o auge físico e acelerada após os 30 anos. O Random Forest, baseado em árvores de decisão, adapta-se melhor a essas curvas sem necessidade de transformações poli- nomiais.

- 2. Interações Condicionais: O valor de uma estatís- tica depende do contexto (ex: "Gols"são cruciais para atacantes, mas irrelevantes para defensores). O mo- delo de árvore consegue segmentar essas regras auto- maticamente.

A estratégia de análise baseou-se no cálculo dos Resí- duos (R), definidos como a diferença entre o valor real de mercado e o valor predito pelo modelo (R = Yreal − Yprevisto). Esta métrica foi utilizada não como erro, mas como indicador de ineficiência de mercado: resíduos positi- vos sugerem supervalorização, enquanto negativos indicam oportunidades de investimento.

## 5 Repositório Utilizado

O código fonte, os datasets tratados e os notebooks de análise estão hospedados no GitHub. A organização do repositório segue a estrutura:

- /jogadores: Arquivos CSV com informações dos jo- gadores.

- /tabela: Tabela final dos campeonatos analisados nas temporadas 24/25.

- /extracoes: Scripts em Python de extração dos da- dos dentro do Sofascore.

- /sem pasta: Scripts divididos por liga (analiseNo- meDaLiga.ipynb) e análise geral (analiseComparati- voGeral.ipynb).

Link público: Repositório GitHub [URL 🔗](https://github.com/Parreirass/AnaliseValorDeMercado24_25)


## 6 Resultados e Discussões

A análise foi conduzida em duas frentes: uma verificação interna de cada liga seguida de uma comparação geral, incluindo estatísticas gerais dos torneios e também a união de todos os jogadores observados.

## 6.1.3 Eficiência Financeira dos Clubes

A relação entre o Valor Total do Elenco e os Pontos Con- quistados evidenciou a disparidade de eficiência. O gráfico de dispersão (Scatter Plot) permitiu identificar outliers: clubes que atingiram altas pontuações com orçamentos modestos (alta eficiência) versus clubes com gastos mas- sivos e desempenho mediano. Ferramentas de scouting desenvolvidas no estudo, como o filtro de atributos e a busca nominal, validaram a existência de substitutos téc- nicos mais baratos dentro da própria liga para as posições mais carentes.

## 6.1 Análise interna de cada liga

Para cada uma das quatro ligas (Bundesliga, Premier Le- ague, La Liga e Serie A), foram aplicadas métricas para isolar o desempenho individual do contexto coletivo e ava- liar a gestão de recursos.

## 6.1.1 O Índice Atlas e a Dependência Individual

Para identificar jogadores que sustentam o desempenho de suas equipes, desenvolveu-se o Índice Atlas (IAtlas), referenciando o titã da mitologia grega conhecido por sua força e a famosa imagem carregando o mundo. A métrica calcula o diferencial entre a nota individual do atleta e a média da equipe:

Os resultados mostraram que o IAtlas é frequentemente mais alto em equipes da metade inferior da tabela. Joga- dores com IAtlas > 0.5 nessas equipes foram classificados como "Atlas", indicando que sua performance individual está dissociada da má fase coletiva, tornando-os alvos pri- mários para transferências.

*Figura 2: Gráfico de Pontos Conquistados X Investimento Total (€) da La Liga*

A Figura 2 evidenciou um exemplo de time que soube investir o seu capital. O Barcelona foi um dos times com o investimento mais modesto do campeonato e, mesmo assim, conseguiu conquistar o título da La Liga 24/25. [URL 🔗](#page-0)

## 6.2 Análise Comparativa Global

Ao unificar as bases de dados, foi possível traçar o perfil econômico e demográfico do futebol europeu.

## 6.2.1 A Inflação da Premier League

A comparação direta do "Custo da Nota SofaS- core"confirmou a hipótese de inflação no mercado inglês. Um jogador com nota média 7.0 na Premier League possui um valor de mercado, em média, 40% a 60% superior a um jogador com a mesma nota na Serie A ou La Liga. Isso indica que o preço de um ativo é determinado tanto pela sua qualidade intrínseca quanto pelo poder de compra da liga onde atua.

*Figura 1: Exemplo dos jogadores "Atlas"da Bundesliga*

## 6.1.2 Categorização de Ativos: Diamantes vs. Luxo

Com base na relação entre custo, desempenho e posição na tabela, os jogadores foram segmentados em duas cate- gorias críticas:

- Diamantes: Jogadores com alta performance (Nota > 7.15) atuando em times posicionados abaixo do 10º lugar. Estes representam a máxima eficiência técnica.

- Luxo Desperdiçado: Jogadores com valor de mer- cado superior a €30 milhões atuando em equipes de baixa performance. A análise revelou uma concentra- ção destes casos na Premier League, sugerindo inefi- ciência na alocação de recursos de clubes ingleses de médio porte.

*Figura 3: Distribuição de valor de mercado por liga*

A Figura 3 evidencia a diferença de valor de mercado médio entre os jogadores da premier league em compara- ção com as demais ligas. Isso indica que os melhores joga- dores do mundo estão concentrados lá, porém, ao mesmo tempo, concentra muitos jogadores supervalorizados. [URL 🔗](#page-0)


## 6.2.2 Demografia e Estilo de Jogo

A análise de distribuição de idade ("Onde jogam os jo- vens e os veteranos") confirmou a Bundesliga como a liga com menor média de idade, consolidando-se como um polo de desenvolvimento de talentos. Em contraste, a Serie A apresentou uma curva demográfica deslocada para a di- reita, indicando maior valorização da experiência. O com- parativo de médias estatísticas por jogador (Gols, Assis- tências, Desarmes) revelou o "DNA"de cada liga, com a Bundesliga apresentando médias ofensivas superiores, en- quanto La Liga destacou-se pela métrica de passes e posse.

## 6.2.3 Seleção Ideal e Atributos de Elite

A formação da "Seleção da Europa", baseada puramente em notas estatísticas, resultou em uma equipe heterogê- nea, provando que o talento de elite está distribuído entre as ligas, apesar da concentração financeira na Inglaterra. A mineração de texto nos atributos dos jogadores mais va- liosos (Top 10% financeiro) revelou que características cog- nitivas e técnicas ("Visão de Jogo", "Passe", "Técnica") são mais frequentes na elite do que atributos puramente físicos, sugerindo que o mercado paga um prêmio pela in- teligência de jogo.

## 6.3 Modelagem de Valuation: Justifica- tiva de Preço de Ativos

Para determinar o "Preço Justo"e identificar oportunida- des de mercado, comparou-se o desempenho de dois mode- los: Regressão Linear Múltipla e Random Forest Regres- sor.

## 6.3.1 Correlação e Drivers de Valor

A matriz de correlação demonstrou que "Gols"e "Assis- tências"são os maiores impulsionadores de valor (r > 0.6). Crucialmente, a variável "Idade"apresentou correlação ne- gativa, confirmando que o valor de mercado penaliza o en- velhecimento, independentemente da manutenção da per-

formance técnica.

## 6.3.2 Superioridade do Random Forest

O modelo Random Forest apresentou um coeficiente de determinação (R2) significativamente superior à Regres- são Linear. Esta superioridade técnica justifica-se por três fatores que o modelo linear falhou em capturar:

- 1. Não-Linearidade da Idade: A relação entre idade e valor não é uma reta, mas uma curva (valorização até o auge físico, seguida de declínio). O Random Forest modelou essa curva com precisão, enquanto a regressão linear tendia a subestimar jovens talentos e superestimar veteranos.

- 2. Interações Condicionais: O valor de uma es- tatística depende da posição (contexto). O Ran- dom Forest identificou automaticamente que "Desar- mes"valorizam defensores, mas são irrelevantes para atacantes.

- 3. Resiliência a Outliers: O modelo de floresta li- dou melhor com os valores extremos dos "supercra- ques"(€100M+), evitando que estes distorcessem a predição para a média dos jogadores.

## 6.3.3 Análise de Resíduos: O Veredito do Modelo

A análise final baseou-se nos resíduos do Random Forest (ValorReal −ValorJusto).

- Supervalorizados: Jogadores com resíduos positi- vos altos. Geralmente atletas de grife em ligas infla- cionadas, cujo desempenho estatístico não justifica o preço de etiqueta.

- Subvalorizados (Oportunidades): Jogadores com resíduos negativos. Identificou-se aqui um nicho de atletas de alta performance em ligas menos ricas (como Serie A) ou em times menores, que o modelo avaliou como "descontados"pelo mercado.

*Figura 4: Preço de Mercado X Preço Justo Calculado (Via Random Forrest)*

## 7 Conclusão e Considerações Fi- nais

O trabalho atingiu seu objetivo principal ao estabelecer um fluxo de análise de dados robusto para o futebol euro- peu. Foi possível demonstrar que o valor de mercado de um jogador é uma variável complexa, influenciada tanto por sua performance técnica quanto pelo contexto econô- mico da liga onde atua.

A implementação dos dicionários de correção de nomes e o tratamento de transferências foram fundamentais para a confiabilidade dos resultados, mitigando um problema comum em datasets públicos. O modelo de Regressão Li- near, embora simples, provou-se eficaz como ferramenta inicial de valuation, servindo de base para a detecção de anomalias de mercado.

Como limitações, cita-se a ausência de dados físicos, his- tórico de lesões, presença em seleções e a natureza estática da análise (recorte apenas da temporada passada). Traba- lhos futuros podem expandir este escopo para incluir séries temporais, analisando a evolução do valor de mercado ro- dada a rodada, ou aplicar modelos mais complexos com um maior número de dados de cada jogador e informações sobre histórico das ligas.


## Referências

- [1] SofaScore. Database de Estatísticas de Futebol. Acesso em: Dezembro de 2025. Disponível em: https://www.sofascore.com/pt/ [URL 🔗](https://www.sofascore.com/pt/)

- [2] Pandas Development Team. pandas: data analysis to- ols for the Python programming language. 2025.
