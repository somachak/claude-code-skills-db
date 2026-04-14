---
name: building-event-driven-services
description: Designs event-driven services with explicit contracts, delivery semantics, replay handling, and consumer isolation. Use when adopting queues, streams, outbox patterns, or domain events.
when_to_use: event driven, kafka, queue design
allowed-tools: Read Grep Bash
---

## Event-Driven Architecture and Messaging

Event-driven decouples services. One service publishes "OrderCreated"; others subscribe and react asynchronously. Common in microservices, real-time systems, and event sourcing.

### When to Use

- Designing a multi-service system (order → payment → notification → analytics)
- Building real-time features (notifications, live updates)
- Event sourcing or audit logs
- Decoupling services to improve resilience

### Decision Framework for Node.js/Python + Message Broker (RabbitMQ, Kafka, AWS SNS/SQS)

1. **Choose the right broker.** RabbitMQ: complex routing, dead-letter queues, good for job queues. Kafka: high throughput, event stream, ordered processing, good for audit logs. SNS/SQS: AWS-managed, simpler.
2. **Event schema must be versioned.** Events evolve. Use Avro, JSON Schema, or Protobuf. Consumers must handle new fields gracefully (forward compatibility).
3. **Idempotency is critical.** Event published twice? Consumer processes it safely twice. Use event ID + idempotency key.
4. **Dead-letter queue for failures.** Event processing fails? Send to DLQ. Manual inspection and replay later.
5. **Consumer groups for scalability.** In Kafka, multiple consumers in the same group partition the load. RabbitMQ uses competing consumers.

### Anti-patterns to Avoid

- No event versioning. Add a field to an event; old consumers break.
- Tight coupling between event publisher and subscribers. Publisher doesn't know who cares; subscribers subscribe to event topic, not a publisher-specific queue.
- Processing events synchronously. Event handler blocks; slow handler = slow event propagation. Use async processing.
- No idempotency. Event published twice = action taken twice. Use event ID to track processed events.

### Checklist

- [ ] Event schema is defined and versioned (Avro, JSON Schema, or Protobuf)
- [ ] Publisher doesn't know subscribers; publishes to a topic/exchange
- [ ] Subscriber handles unknown fields (forward compatibility)
- [ ] Event processing is idempotent (same event ID = same result)
- [ ] Dead-letter queue captures unprocessable events
- [ ] Failed event processing is logged and alerted
- [ ] Consumer group or competing consumer pattern is used for scaling
- [ ] Test: publish event, consumer fails, event is retried; verify it's safe
- [ ] Monitor: event publishing latency, consumption lag, failure rate
