# Sistema de Gestão de Estoque

Este projeto é um sistema de gestão de estoque desenvolvido em Django.

Ele permite o gerenciamento de produtos, fornecedores, saídas e entradas de estoque, além de fornecer uma interface administrativa para facilitar a gestão.

## Funcionalidades

- **Gerenciamento de Marcas**: Criação, atualização, visualização e exclusão de marcas.

- **Gerenciamento de Categorias**: Criação, atualização, visualização e exclusão de categorias.

- **Gerenciamento de Produtos**: Criação, atualização, visualização e exclusão de produtos.
  
- **Gerenciamento de Fornecedores**: Criação, atualização, visualização e exclusão de fornecedores.

- **Gerenciamento de Saídas e Entradas**: Controle das saídas de produtos do estoque por meio do modelo `Outflow`, que registra as saídas associando produtos e fornecedores.

- **Automatização com Signals**: O projeto utiliza signals do Django para automatizar ações em resposta a eventos no sistema.

- **Interface Administrativa**: Painel de administração para gerenciar produtos e fornecedores, permitindo fácil acesso às funcionalidades principais.

- **Filtros de Busca**: Possibilidade de filtrar produtos e fornecedores por nome, número de série, categoria e marca.

- **Métricas de Vendas**: Visualização de métricas relacionadas a produtos e vendas, ajudando na análise de desempenho através de gráficos utilizando Chart.JS.

- **Controle de Acesso**: O sistema implementa um controle de acesso baseado em permissões. As views são protegidas por mixins como `LoginRequiredMixin` e `PermissionRequiredMixin`, garantindo que apenas usuários autenticados e autorizados possam acessar certas funcionalidades. Exemplos:
  - **Visualização de Produtos e Fornecedores**: Apenas usuários com a permissão `view_product` ou `view_supplier` podem acessar as listas correspondentes.
  - **Criação, Atualização e Exclusão**: Usuários precisam das permissões `add_product`, `change_product`, e `delete_product` para realizar essas ações.

## Testes Unitários

O projeto inclui testes unitários para garantir a funcionalidade das views, models e outros componentes do sistema. Os testes verificam:

- A listage, criação, atualização e exclusão de todas as apps.
- A integridade das funções de saída e entrada de estoque.
- O funcionamento correto dos signals, garantindo que as quantidades de produtos sejam atualizadas corretamente.
- O funcionamento das permissões de usuários.

# Tecnologias Utilizadas

* Python
* Django
* HTML
* JavaScript
* Chart.JS
* SQLite

## Bibliotecas Utilizadas

Estão listadas no arquivo requirements.txt

# Como executar o projeto
Pré-requisitos: Python 3.11+

```python
# Realizar o clone desse repositório e acessar a pasta onde foi gerado:
git clone https://github.com/Samaelpicoli/Gestao-Estoque.git

# Criar o ambiente virtual:
python -m venv venv | python3 -m venv venv

# Ativar o ambiente virtual:

# Linux:
source venv/bin/activate

# Windows:
.\venv\Scripts\activate

#insalar dependências, dentro do seu projeto e com ambiente virtual ativo:
pip install -r requirements.txt

# executar o código contrib/env_gen.py para geração do arquivo .env:
python contrib/env_gen.py

# Realizar as migrações
python manage.py migrate

# Criar um superusuário para realizar login
python manage.py createsuperuser

# Executar os testes:
python manage.py test / coverage run manage.py test / task test

# Visualizar a cobertura de testes:
coverage html

# Executar o sistema:
python manage.py runserver
```

# Autor
Samael Muniz Picoli
