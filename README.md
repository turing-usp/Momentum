# Momentum

Este repositório contém a implementação da estratégias de investimento Momentum, feita pelos membros do Grupo Turing Quant. Implementação baseada no paper: [Time Series Momentum](http://docs.lhpedersen.com/TimeSeriesMomentum.pdf) by Tobias J. Moskowitza, Yao Hua Ooi and Lasse Heje Pedersen.

## Uso

Para Para seu pleno uso, são necessárias algumas outras bibliotecas e credenciais. Para isso use o pip para instalar alguns pacotes em seu environment:

`pip install pandas pandas_datareader numpy matplotlib`

 - O dataset foi omitido

## Funções implementadas

- `prepare_yahoo_df` - Constroi o dataframe da maneira utilizada nas demais funções
- `parkinson_vol` - Estima a volatilidade a partir dos preço de Alta e de Baixa
- `garman_klass_vol` - Estima a volatilidade a partir dos seguintes preços: alta, baixa, abertura e fechamento
- `tsmom` - Simula a estrátegia de investimento em um período, retorna a rentabilidade no período simulado.
- `csmom`- Simula a estrátegia de investimento em um período, retorna a rentabilidade no período simulado.
- `signal` - Constroi o vetor de sinais Long ou Short no período simulado.
- `backtesting` - Realiza o backtesting em grande períodos.

## Feito por:
 - Lucas Leme Santos 
