<p align="center">
  <p align="center">
    <a href="https://purplship.com" target="_blank">
      <img src="https://github.com/Purplship/purplship-server/raw/main/purpleserver/purpleserver/static/extra/branding/icon.png" alt="Purplship" height="100">
    </a>
  </p>
  <h2 align="center">
    The Open Source Multi-carrier Shipping API
  </h2>
  <p align="center">
    <a href="https://github.com/Purplship/purplship-server/actions"><img src="https://github.com/Purplship/purplship-server/workflows/puprlship-server/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://www.gnu.org/licenses/agpl-3.0" rel="nofollow"><img src="https://camo.githubusercontent.com/cb1d26ec555a33e9f09fe279b5edc49996a3bb3b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4147504c25323076332d626c75652e737667" alt="License: AGPL v3" data-canonical-src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" style="max-width:100%;"></a>
  </p>
</p>


## What's Purplship?

Purplship server is an On-prem or cloud Multi-carrier Shipping API.
The server is in Python, but you can use any programming language to send API requests to 
any supported shipping carriers (Canada Post, DHL, FedEx, UPS, Purolator...), from your application.

- [Schedule a Live Demo](https://purplship.com/schedule-demo/)
- [Join us on Discord](https://discord.gg/kXEa3UMRHd)


## Screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/Purplship/purplship-server/main/artifacts/dashboard1.png" width="400">
  <img src="https://raw.githubusercontent.com/Purplship/purplship-server/main/artifacts/dashboard2.png" width="400">
</p>


## Deployment

### `Docker`

<details>
<summary>Deploy with docker compose</summary>

```yaml
version: '3'

services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"

  purplship:
    image: purplship/purplship-server:[version]
    restart: always
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=db
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    ports:
      - "5002:5002"
    depends_on:
      - db
```

</details>

OR use our image 

<details>
<summary>Run an instance of Postgres image</summary>

```bash
docker run -d --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres
```

</details>

```bash
docker run --rm --name purplship --link=db:db -p5002:5002 purplship/purplship-server:[version]
```

### `Heroku`

Host your own Purplship server for FREE with [One-Click Deploy](https://heroku.com/deploy).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Purplship/purplship-heroku/tree/main/)


## Official Client Libraries

- [Node](https://github.com/Purplship/purplship-node)
- [PHP](https://github.com/Purplship/purplship-php-client)
- [Python](https://github.com/Purplship/purplship-python-client)

Use the [swagger editor](https://editor.swagger.io/) to generate any additional client with our [OpenAPI References](https://github.com/Purplship/purplship-server/tree/main/openapi)


## Resources

- **Documentation** - Learn more at [docs.purplship.com](https://docs.purplship.com)
- **Community** - Feature requests, general questions on [Discord](https://discord.gg/kXEa3UMRHd)
- **Bug Tracker** - [File bugs](https://github.com/Purplship/purplship-server/issues)
- **Blog** - Get the latest updates from the [Puprlship blog](https://blog.purplship.com).
- **Twitter** - Follow [Purplship](https://twitter.com/purplship).


## License

This project is licensed under the terms of the `AGPL v3` license.

We also release a community image under the `Apache 2` license.

See the [LICENSE file](/LICENSE) for license rights and limitations.

Any other questions, mail us at hello@purplship.com. We’d love to meet you!