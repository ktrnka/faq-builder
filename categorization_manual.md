# Content Categorization Manual

## Purpose

This manual defines the standardized categorization system for analyzing Keith's Reddit posts and YouTube content to identify blog post clusters. Each piece of content is classified along three dimensions: Topic, Domain, and Audience.

## Classification Framework

### Topic Categories

**Core Technical Topics:**
- `concept-explanation` - Breaking down complex technical ideas into understandable components
- `tool-selection` - Comparing frameworks, libraries, services, or approaches 
- `model-evaluation` - Assessment methodologies, metrics, validation techniques
- `data-management` - Pipeline design, data quality, annotation, versioning
- `ml-deployment` - Production systems, MLOps, monitoring, CI/CD
- `research-methodology` - Experimental design, statistical practices, reproducibility
- `infrastructure-setup` - System configuration, DevOps, cloud deployment
- `troubleshooting` - Debugging strategies, problem resolution, error analysis

**Application Areas:**
- `nlp-applications` - Natural language processing, text analysis, language models
- `healthcare-ai` - Medical applications, clinical systems, regulatory considerations
- `low-resource-ml` - Limited data scenarios, underrepresented languages/domains
- `ai-safety-ethics` - Responsible AI practices, bias mitigation, fairness
- `data-privacy` - HIPAA compliance, synthetic data, regulatory requirements

**Professional Development:**
- `career-transition` - Career guidance, job changes, industry transitions
- `academic-guidance` - Educational direction, research topics, thesis advice
- `management-advice` - Technical leadership, project management, team coordination
- `industry-insights` - Market trends, technology adoption, business perspectives

**Project and Process:**
- `academic-projects` - University coursework, research work, thesis projects
- `team-processes` - Workflow optimization, collaboration methods, knowledge sharing

### Domain Categories

**Primary Domains:**
- `general-tech` - Broadly applicable across industries and contexts
- `healthcare` - Medical technology, clinical applications, health systems
- `academic` - Research institutions, educational contexts, scholarly work
- `gaming` - Game development, entertainment technology, interactive media

**Secondary Domains (use sparingly):**
- `startup` - Early-stage company considerations and constraints
- `enterprise` - Large organization challenges and requirements
- `finance` - Financial services applications and regulatory requirements

### Audience Categories

**Primary Audiences:**
- `beginners` - New to programming, AI/ML, or data science
- `practitioners` - Working data scientists, ML engineers, software developers
- `researchers` - Academic researchers, graduate students, research-focused professionals
- `managers` - Technical leaders, project managers, decision makers
- `career-changers` - Professionals transitioning between fields or roles

## Classification Guidelines

### Topic Selection Rules:
1. **Primary focus first** - Choose the main technical or professional topic
2. **Maximum 3 topics** - Avoid over-tagging; focus on most relevant aspects
3. **Specific over general** - Prefer `nlp-applications` over `concept-explanation` when NLP is central
4. **Technical over meta** - Prefer technical topics over process topics when both apply

### Domain Selection Rules:
1. **Context-driven** - Consider where the advice would be most applicable
2. **Keith's experience** - Prefer domains where Keith has demonstrated expertise
3. **Default to general-tech** - When domain is unclear or broadly applicable
4. **Single domain only** - Choose the most relevant domain context

### Audience Selection Rules:
1. **Knowledge requirements** - Consider technical background needed to understand content
2. **Professional context** - Consider career stage and role relevance
3. **Maximum 3 audiences** - Focus on primary target audiences
4. **Inclusive when appropriate** - Include `beginners` when content is accessible

## Common Patterns

### Reddit Content Typically Features:
- Technical problem-solving → `concept-explanation`, `troubleshooting`
- Tool comparisons → `tool-selection`
- Career questions → `career-transition`, `academic-guidance`
- Research methodology → `research-methodology`, `model-evaluation`

### YouTube Content Typically Features:
- Live problem-solving → `troubleshooting`, `concept-explanation`
- Career discussions → `career-transition`, `management-advice`
- Project walkthroughs → `infrastructure-setup`, `team-processes`
- Industry insights → `industry-insights`, `management-advice`

## Example Classifications

**Reddit: Support KB Chatbot Training**
- Topics: `tool-selection`, `nlp-applications`
- Domain: `general-tech`
- Audience: `practitioners`, `beginners`

**YouTube: Healthcare AI Project Discussion**
- Topics: `management-advice`, `healthcare-ai`, `team-processes`
- Domain: `healthcare`
- Audience: `practitioners`, `managers`

**Reddit: Career Transition Question**
- Topics: `career-transition`, `academic-guidance`
- Domain: `general-tech`
- Audience: `career-changers`, `beginners`

## Migration Notes

When updating existing classifications:
1. Consolidate similar topics (e.g., `career-guidance` → `career-transition`)
2. Separate domain from topic (e.g., `healthcare-ai` topic becomes `healthcare` domain + `nlp-applications` topic)
3. Standardize spelling and formatting
4. Remove overly specific one-off categories
5. Ensure consistency with manual guidelines