# relatorio_tri-llm

* Para iniciar, vá para a pasta:
```
cd reports
```
* Execute o arquivo "cria_input_aluno.py" para salvar informações de 8 alunos aleatórios respondendo 8 itens aleatórios na pasta "input_info"
```
python cria_input_aluno.py
```

## Prompt para o LLM na geração de relatórios para **ALUNOS**:
```
Suas tarefas:

1. Ler um arquivo da pasta "input_info";
2. Ler o arquivo "prompt_aluno_opencode.txt";
3. No "prompt_aluno_opencode.txt", seguir as regras estabelecidas ;
4. Adicionar ao template de html presente no "prompt_aluno_opencode.txt" um ponto chamado "Materiais relevantes" dentro da seção "Estratégias de Estudo Direcionadas":
4.1. Este ponto tem como objetivo indicar materiais de estudo da internet pertinentes ao assunto contido nas habilidades e competências exigidas presentes no html;
4.2. Este ponto deve conter links retirados da internet divididos em 3 categorias:
4.2.1. Videoaulas;
4.2.2. Páginas da internet explicativas (exclui-se páginas do gov.br);
4.2.3. PDFs ou slides referentes ao assunto (não obrigatório).
5. Com essas alterações, você deve gerar um arquivo html independente nomeado da seguinte forma: "relatorio_{MATRICULA}_{ITEM_PROVA}_{ESTADO}_{AREA}.html":
5.1. Este arquivo html deve ser relacionado somente aos dados presentes no arquivo correspondente na pasta "input_info";
5.2. Este arquivo html deve seguir a estrutura do html presente no "prompt_aluno_opencode.txt";
6. O arquivo html gerado deve ser salvo na pasta "student_reports". Se ela não existir, você deve criá-la;
7. O processo deve ser repetido desde o passo '1.' para todo arquivo da pasta "input_info" e tire dúvidas, se tiver.
```

## Prompt para o LLM na geração de relatórios para **PROFESSORES**:
```
Execute as seguintes tarefas:

1. Leia o arquivo "prompt_prof_opencode.txt";
2. Sem alterar o arquivo, gere um arquivo html com as seguintes alterações:
2.1. Adicione textos contendo a análise exigida em cada parte do HTML;
2.2. Explique os dados apresentados de forma coesa que se encaixe na estrutura já existente;
2.3. O output deve ser um arquivo HTML puro que deve ser salvo na pasta "prof_reports" (se ela não existir, crie-a).
3. Este HTML deve apresentar a mesma estrutura apresentada no arquivo "prompt_prof_opencode.txt", apenas com as mudanças já solicitadas.
```
# relatorio_tri-llm
