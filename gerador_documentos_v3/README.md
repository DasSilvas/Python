# Gerador de Documentos — v3 (especialidades por subpastas)

## Organização

```text
Gerador_Documentos/
├── app.py
├── templates/
│   ├── Estabilidade/
│   │   ├── Memoria_Descritiva.docx
│   │   └── Termo_Responsabilidade.docx
│   └── Esgotos_Domesticos/
│       ├── Memoria_Descritiva.docx
│       └── Termo_Responsabilidade.docx
└── output/
```

Cada subpasta direta de `templates` é uma especialidade. Cada ficheiro `.docx` nessa subpasta aparece na UI com o seu nome real. Não é necessário editar JSON nem código para adicionar uma especialidade.

## Instalação

```bash
pip install pandas openpyxl docxtpl tkinterdnd2
python app.py
```

## Excel e modelos

O Excel mantém o formato anterior: a primeira linha é ignorada; a coluna A contém o nome do parâmetro e a coluna B o valor. Os nomes devem corresponder aos marcadores dos modelos Word, por exemplo `{{ cliente }}`.

Os modelos são preenchidos com `DocxTemplate`, preservando a abordagem do código original.

## Exportação

Os documentos são guardados na pasta de destino com o formato:
`NomeDaEspecialidade_NomeDoModelo.docx`

Este prefixo evita colisões se duas especialidades tiverem ficheiros com o mesmo nome, por exemplo ambas com `Memoria_Descritiva.docx`.

## Comportamento

- As especialidades são descobertas quando a aplicação abre.
- A seleção nunca é guardada; ao abrir a aplicação, começa tudo desmarcado.
- Não existe histórico.
- A aplicação permanece aberta após gerar documentos.
- Só são consideradas subpastas imediatas de `templates`, não subpastas aninhadas.
- O código foi verificado quanto à sintaxe, mas deve ser testado com os modelos reais.
