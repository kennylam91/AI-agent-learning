# Agent Notes

## Agent Loop

A LLM can answer questions. An agent can do things. The agent loop is what makes that difference possible.

When a model receives a request it cannot fully address with its training alone, it needs to reach out into the world: read files, query databases, call APIs, execute code. The agent loop is the orchestration layer that enables this. It manages the cycle of reasoning and action that allows a model to tackle problems requiring multiple steps, external information, or real-world side effects.

## Messages And Conversation History

Messages flow through the agent loop with two roles: user and assistant. Each message contains content that can take different form.

User messages contain the initial request and any follow-up instructions.

Assistant messages are the model's outputs.

## Tool Execution

## Loop Lifecycle

The agent loop has well-defined entry and exit points.

## Stop Reasons

* End turn
* Tool use
* Max tokens
* Stop sequence
* Content filtered
* Guardrail intervention
