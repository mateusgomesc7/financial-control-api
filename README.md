# Financial Control API

Este repositório contém a API do projeto **Financial Control**, desenvolvida com Python e gerenciada pelo **Poetry**. A aplicação é containerizada utilizando **Docker** para facilitar o desenvolvimento e a implantação.

## Requisitos

Certifique-se de ter os seguintes itens instalados em seu ambiente:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)

## Configuração do Ambiente

1. Instale as dependências usando o Poetry:

   ```bash
   poetry install
   ```

2. Crie um arquivo `.env` com base no arquivo `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Configure as variáveis de ambiente conforme necessário.

## Uso com Docker

### Construir a imagem Docker

Para construir a imagem da aplicação, execute:

```bash
docker-compose build
```

### Rodar a aplicação

Inicie os contêineres com o seguinte comando:

```bash
docker-compose up
```

A API estará acessível em `http://localhost:8000`.

### Parar os contêineres

Para interromper os contêineres, use:

```bash
docker-compose down
```

## Testes

Para rodar os testes, execute:

```bash
make test
```

## Contribuição

1. Faça um fork deste repositório.
2. Crie uma branch para sua feature/bugfix: `git checkout -b minha-feature`.
3. Commit suas alterações: `git commit -m 'Minha nova feature'`.
4. Envie suas alterações: `git push origin minha-feature`.
5. Abra um Pull Request.
