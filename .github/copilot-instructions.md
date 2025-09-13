# Copilot Instructions

## Project Overview
See the README.md

## Interaction Guidelines
- When making design decisions that will significantly affect future development, consider how it will fit into the long-term vision and ask for feedback on the approach.
- If instructions don't seem feasible (e.g., extracting data that doesn't exist in the source, conflicting requirements), stop development and ask for guidance rather than making assumptions. Clear communication prevents wasted effort and ensures the right solution.
- **For bug reports and data quality issues**: Always start with TDD - create a failing test that reproduces the problem before attempting any fixes
- **For new features**: Ask whether to use TDD or implement directly, depending on complexity and risk
- After completing a major feature or refactor, do a small post-mortem. Reflect on what went well and what could be improved. Then consider some small incremental changes to our development process that might improve our workflow. Then review them with me and collaborate to update the copilot instructions.

## Code Design Principles

### Architecture & Testing Philosophy
- **Functional Core, Imperative Shell**: Naturally separate conditional business logic (functional core) from I/O operations, API calls, database interactions, and user interfaces (imperative shell)
- **Test What Can Meaningfully Fail**: Focus tests on business logic and complex conditional behavior, not framework functionality or simple property access
- **Avoid Mocking**: If tests require mocking, that's usually a sign of poor separation of concerns. Flag this as an architectural issue and suggest refactoring, or note as future work if in deep development
- **Minimal Viable Testing**: Keep a small set of focused tests for basic coverage (catching syntax errors) and complex business logic maintenance

### File Organization & Structure
- **Co-locate Tightly Coupled Code**: Keep related functionality in the same file rather than over-separating into many small files
- **Bias Toward Simplicity**: Start with minimal viable implementation, then add structure as complexity demands it
- **Development Stage Awareness**: Adjust complexity and structure based on exploration vs. mature implementation phases

### Design Documentation
- **Keep It Conceptual**: Focus on the "why" behind decisions rather than detailed code examples
- **Err on the Side of Short**: Concise design docs that won't become maintenance burdens
- **Minimize Code Examples**: Include code in design docs only when specifically requested
- **Timeless Content**: Design docs should be resilient to frequent code modifications

### Testing Strategy by Context
- **Early Exploration**: Focus on import tests and basic smoke tests, add business logic tests once approach is solidified
- **Business Logic**: Write unit tests for complex conditional logic that's separated from I/O
- **API/Integration**: Implement first, then test through actual usage rather than extensive mocking
- **Test the Functional Core**: Target tests at the pure logic functions, not the imperative shell

### Implementation Approach
- **Context-Dependent Strategy**: Ask for clarification when implementation approach is unclear
- **Natural Separation**: Don't over-engineer separation of concerns upfront; let it emerge naturally during coding
- **Question Timing**: If unsure whether to test-first or implement-first, consider the risk profile (complex logic = test-first, API integration = implement-first)

