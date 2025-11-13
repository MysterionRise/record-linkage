# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository focuses on **record linkage** - the process of identifying pairs of records that refer to the same entity (typically people) across datasets. It includes research, documentation, and planned implementations of various approaches to this problem.

### Key Concepts

**Record Linkage**: Identifying which records in a dataset (or across multiple datasets) refer to the same real-world entity. Common use cases:
- Deduplication (avoiding sending mail to the same person multiple times)
- Patient tracking across hospital visits
- Cross-dataset entity resolution

**Entity Linking**: A subset of record linkage focused specifically on linking entities based on their names (e.g., "John Kennedy", "J. F. K", "Джон Кеннеди" as the same person).

## Current Repository State

The repository is currently in a **documentation and planning phase**. Previous implementations in Python and Scala have been removed (see git history). The .gitignore indicates planned support for:
- JVM languages (Scala/Java) using sbt or Gradle
- Haskell
- R

## Planned Approaches

### Name Matching (see name-matching/README.md)

Entity linking via information retrieval:
1. **OpenSearch installation** - Using search infrastructure
2. **Zentity plugin** - Entity resolution plugin for Elasticsearch/OpenSearch
3. **Search strategies**:
   - Synonym files approach (large synonym dictionaries for name variations)
   - Knowledge graph approach (exploiting entity relationships)

### General Approaches (see main README.md)

- **Text-based approaches**: Extract textual features from large corpora
- **Graph-based approaches**: Exploit knowledge graph structure to represent entity context and relationships

## Key Resources

The README.md contains links to important academic papers and resources on record linkage:
- Bristol University probabilistic linkage guide
- ArXiv papers on entity linking
- O'Reilly presentations on record linkage
- UCI Machine Learning Repository datasets for record linkage
- Febrl (Freely Extensible Biomedical Record Linkage) documentation

## Development Notes

When implementing code in this repository:
- The focus is on entity resolution and record linkage algorithms
- Multiple language implementations may coexist (based on .gitignore patterns)
- Consider both text-based and graph-based approaches
- Entity linking solutions should handle name variations, transliterations, and abbreviations
- OpenSearch/Elasticsearch integration is a planned implementation path
