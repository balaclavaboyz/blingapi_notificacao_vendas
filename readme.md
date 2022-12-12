# bomdia

## para que server isso

toda vez que uma nota fiscal eh gerado e mandado na aba de vendas e dentro de nota fiscais, com o status de Pendente, eh mandado um email com o aviso.

o unico arquivo que eh preciso criar eh o .env, la voce colocar as variaveis APIKEY, MEUEMAIL, MINHASENHA e STATUS
```
APIKEY=1234789
MEUEMAIL=teste@teste.com.br
MINHASENHA=12345321
STATUS=Pendente
```
coloquei STATUS Pendente, porque eh o unico momento que a venda eh concretizado

primeiro tem que rodar pelo menos uma vez pra salvar as informacoes em arquivos antes de rodar ele definidamente

usar o scheduler do windows para a execucao automatico

no scheduler do windows, coloquei pra rodar cada 15 min por 8 horas