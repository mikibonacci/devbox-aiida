# RabbitMQ Basics — Python Edition

---

## Concepts

| Term | What it is |
|------|-----------|
| **broker** | The RabbitMQ server — receives, routes, and stores messages |
| **producer** | Code that sends messages |
| **consumer** | Code that receives and processes messages |
| **queue** | A named buffer where messages wait to be consumed |
| **exchange** | A router — receives messages from producers and puts them in queues |
| **binding** | The rule that connects an exchange to a queue |
| **channel** | A lightweight connection multiplexed over one TCP connection |

Default ports:
- **5672** — AMQP (the protocol Python uses to talk to RabbitMQ)
- **15672** — Management HTTP API / web UI (if plugin enabled)

---

## Check the port

```bash
# Check if RabbitMQ is listening
rabbitmq-diagnostics listeners

# Quick check with netstat/lsof
lsof -i :5672          # macOS
ss -tlnp | grep 5672   # Linux

# Check via the CLI tool
rabbitmqctl status | grep -A5 "listeners"

# If the management plugin is enabled, the web UI is at:
# http://localhost:15672  (default login: guest / guest)
```

Example output of `rabbitmq-diagnostics listeners`:

```
Interface: [::], port: 25672, protocol: clustering, purpose: inter-node and CLI tool communication
Interface: [::], port: 5672,  protocol: amqp,       purpose: AMQP 0-9-1 and AMQP 1.0
```

What each line means:

| Port | Protocol | What uses it |
|------|----------|-------------|
| **5672** | `amqp` | Your Python code (`pika`), AiiDA, any AMQP client — **this is the one you care about** |
| **25672** | `clustering` | Internal RabbitMQ CLI and inter-node communication — ignore this in application code |

`[::]` means RabbitMQ is listening on all network interfaces (both IPv4 and IPv6).
So to connect from Python, use `host='localhost', port=5672`.

---

## Install the Python client

```bash
pip install pika
```

`pika` is the standard pure-Python AMQP client for RabbitMQ.

---

## Connect

```python
import pika

# Connect to local RabbitMQ (default port 5672)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()
```

With credentials:

```python
credentials = pika.PlainCredentials('myuser', 'mypassword')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()
```

---

## Send a message (producer)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue (creates it if it doesn't exist)
channel.queue_declare(queue='hello')

# Publish a message to the default exchange, routing to queue 'hello'
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello World!'
)

print("Sent: Hello World!")
connection.close()
```

---

## Receive messages (consumer)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')  # safe to declare again — idempotent

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True   # automatically acknowledge receipt
)

print("Waiting for messages. CTRL+C to stop.")
channel.start_consuming()  # blocks forever, calling callback on each message
```

---

## Manage users & vhosts from the CLI

```bash
# List users
rabbitmqctl list_users

# Create a user
rabbitmqctl add_user myuser mypassword

# Give the user admin rights
rabbitmqctl set_user_tags myuser administrator

# Create a virtual host (namespace for queues/exchanges)
rabbitmqctl add_vhost myvhost

# Grant the user full permissions on that vhost
rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

# List queues (on the default vhost /)
rabbitmqctl list_queues

# List queues on a specific vhost
rabbitmqctl list_queues -p myvhost name messages
```

---

## Enable the management web UI

```bash
rabbitmq-plugins enable rabbitmq_management
# Then open: http://localhost:15672
# Default credentials: guest / guest (only works from localhost)
```

---

## Connection URL shorthand

Many libraries (including AiiDA) accept a single URL instead of separate params:

```
amqp://myuser:mypassword@localhost:5672/myvhost
```

In Python with pika:

```python
import pika

params = pika.URLParameters('amqp://myuser:mypassword@localhost:5672/myvhost')
connection = pika.BlockingConnection(params)
```
