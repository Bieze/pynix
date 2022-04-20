# Setup

Rename the config from config.example.toml to
config.toml. Replace the token with your bot token.

# How to setup database connection

Pynix runs using a PostgreSQL database and to connect to that
database you must have a user, a database, a password. The bot
will create all the tables by itself.

the dsn is the connection string for the bot. Here are example
details.

user = mike
database = aaron
password = 1234
port = 5432
host = localhost

The connection string would be moved from `postgres://user:password@host:port/database` to
`postgres://mike:1234@localhost:5432/aaron`
