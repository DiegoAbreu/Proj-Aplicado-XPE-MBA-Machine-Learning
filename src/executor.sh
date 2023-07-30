# Ativação de ambiente virtual:
source venv_df_proj/bin/activate
# Documentação Técnica:
## Preparação de arquivos:
rm -rf docs/_build
rm -rf docs/notebooks
cp -r notebooks docs/notebooks/
cp -r references docs/
cd docs 
## Geração de documentação PDF:
#make latexpdf LATEXMKOPTS="-silent"
## Geração de documentação HTML:
make html
## Remoção de arquivos desnecessários:
cd ..
rm -rf docs/notebooks
rm -rf docs/references
cp -r docs/_build/html docs/
rm -rf docs/_build
## Desativação de ambiente virtual
deactivate
## Mensagem de finalização de processamento:
echo ''
echo '---------------------------------'
echo 'Documentação gerada com sucesso!'
echo '---------------------------------'
echo ''