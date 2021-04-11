# Documentation generation bundle

## Setting up database tables

```
console sqlalchemy:table:create lineagebundle.pipeline.Notebook --force
console sqlalchemy:table:create lineagebundle.pipeline.NotebooksRelation --force
console sqlalchemy:table:create lineagebundle.notebook.edge.LineageEdge --force
console sqlalchemy:table:create lineagebundle.notebook.node.LineageNode --force
```
