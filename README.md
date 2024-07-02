# Projeto Kanastra API

Este projeto implementa uma API para processamento de cobranças na plataforma Kanastra. 
A API permite o upload de arquivos CSV contendo informações de débitos, geração de boletos e envio de e-mails aos devedores.

## Configuração do Ambiente

Para configurar o ambiente de desenvolvimento, siga os passos abaixo:

### Pré-requisitos

- Python 3.x
- Docker

### Instalação de Dependências

# Clone o repositório:
```git clone https://github.com/muriloguerreiro/kanastra_api.git ```

```cd kanastra_api```

# Instale as dependências Python (utilizando o Docker):
```docker-compose run web pip install -r requirements.txt```

# Aplique as migrações do banco de dados:
```docker-compose run web python manage.py migrate```

# Construa e execute o projeto com Docker:
```docker-compose up --build```

O servidor estará disponível em `http://localhost:8000/`

### Testando o Projeto

# Para rodar os testes:
```docker-compose run web python manage.py test```

Isso executará todos os testes automatizados para garantir o funcionamento correto da API.

## Endpoints Disponíveis

### Upload de Arquivo CSV

- **URL**: `/billing/upload/`
- **Método**: POST
- **Descrição**: Endpoint para upload de arquivo CSV contendo informações de débitos.

### Listagem de Débitos

- **URL**: `/billing/debts/`
- **Método**: GET
- **Descrição**: Endpoint para listar todos os débitos cadastrados.