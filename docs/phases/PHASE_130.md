# Phase 130: Autonomous Investigation Factory

## GitHub Issue Template

```
## 🚨 Phase 130: Autonomous Investigation Factory

### 📋 Executive Summary
Framework that automates manual investigations by automatically collecting evidence, performing entity correlation, and delivering investigation narratives ready for analyst review when alerts trigger.

### 🎯 Problem Statement
- Manual investigations take hours/days
- Evidence collection is time-consuming
- Inconsistent investigation quality
- Analyst burnout from repetitive work
- Knowledge gaps in complex cases
- Investigation handoffs cause delays

### 💡 Solution
- Automatic evidence collection on alert trigger
- Entity correlation engine
- Investigation workflow automation
- Narrative template system
- Analyst handoff management
- Quality assurance automation

### 🏗️ Technical Architecture
```
src/investigation_factory/
├── factory_orchestrator.py      # Investigation orchestration
├── evidence_collector.py        # Automated evidence collection
├── entity_correlator.py         # Entity correlation engine
├── narrative_generator.py       # Investigation narrative
├── workflow_automation.py       # Workflow automation
├── template_engine.py          # Investigation templates
├── quality_assurance.py        # QA automation
└── handoff_manager.py          # Analyst handoff
```

### ✅ Acceptance Criteria
- [ ] Automatic evidence collection on alert
- [ ] Entity correlation across data sources
- [ ] Investigation narrative generation
- [ ] Quality assurance checks
- [ ] Analyst handoff workflow

### 📊 Impact
- **Investigation Time**: 85% reduction in investigation time
- **Consistency**: 100% consistent investigation quality

### 🏷️ Labels
- `type:feature`, `type:security`, `level:critical`, `size/size/XXL`

---
**Phase**: 130/150
```

## GitHub PR Template

```
## 🚀 PR: Phase 130 - Autonomous Investigation Factory

### 📋 Summary
Automated investigation framework with evidence collection, entity correlation, and narrative generation.

### 📁 Files
- `src/investigation_factory/` - Investigation factory module
- `tests/investigation_factory/` - Tests

---
**Phase**: 130/150
```