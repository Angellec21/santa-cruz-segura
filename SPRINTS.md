# Flujo de sprints (estilo Jira, sobre GitHub)

Este repo usa **Issues + Milestones + un Project v2** para llevar un flujo de sprints
equivalente al que tendríamos en Jira. No hay nada instalado aparte de `gh` (GitHub CLI);
todo el flujo se maneja con comandos.

- **Repo:** `Angellec21/santa-cruz-segura` (permanece en la cuenta personal)
- **Board:** [UPDS-DINAMITA/projects/4](https://github.com/orgs/UPDS-DINAMITA/projects/4) — proyecto de organización, incluye issues de este repo sin necesidad de transferirlo.

---

## Equivalencias Jira ↔ GitHub

| Jira | GitHub |
|------|--------|
| Proyecto | Repo (`Angellec21/santa-cruz-segura`) + Project board en la org `UPDS-DINAMITA` |
| Historia / Tarea / Bug | Issue, clasificada con label `type:*` |
| Épica | (no usado todavía; si hace falta, usar un label `epic:*` o Sub-issues de GitHub) |
| Sprint | Milestone del repo **y** una iteración del campo "Sprint" en el board |
| Backlog del producto | Issues sin milestone asignado, o Status = `Product Backlog` |
| Columnas del tablero (To Do / In Progress / Done / etc.) | Campo "Status" (single select) del Project |
| Story points | (no implementado; se puede agregar un campo Number "Points" si hace falta) |
| Cerrar sprint | Cerrar el milestone + cerrar las issues completadas + mover su Status a `Terminado` |

---

## Estructura actual

### Labels (cada issue lleva exactamente 1 de cada grupo)

- **Tipo:** `type:story`, `type:task`, `type:bug`, `type:chore`
- **Prioridad:** `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- **Componente:** `area:backend`, `area:frontend`, `area:infra`

### Milestones (= Sprints)

- **Sprint 1 - MVP: reportes, mapa de riesgo y autenticación** — cerrado. Documenta
  retroactivamente el MVP ya construido (auth, CRUD de reportes, zonas/mapa, alertas,
  dashboard, IA, notificaciones, deploy inicial).
- **Sprint 2 - Hardening, integraciones reales y calidad** — activo. Tests, CI/CD,
  seguridad, observabilidad e integraciones reales.

### Project board (UPDS-DINAMITA, Board 4)

- **Status** (single select): `Product Backlog` → `En Proceso` → `QA` → `Terminado`
- **Sprint** (iteration, 14 días): una iteración por milestone (`Sprint 1`, `Sprint 2`, ...)
- Vista principal **"Board"**: layout de tablero. Si no aparece agrupada por Status al
  entrar, usar el selector "Group by" de la vista y elegir `Status` — la API de GitHub
  Projects no permite fijar el agrupamiento por defecto de una vista, solo el layout.

---

## Cómo crear un sprint nuevo

1. **Crear el milestone** (ajustar título, fecha de cierre a +14 días y objetivo):

   ```bash
   gh api repos/Angellec21/santa-cruz-segura/milestones \
     -f title="Sprint 3 - <objetivo del sprint>" \
     -f state="open" \
     -f description="<qué cubre este sprint>" \
     -f due_on="$(date -v+14d -u +%Y-%m-%dT23:59:59Z)"   # macOS; en Linux: date -u -d '+14 days'
   ```

2. **Agregar la iteración correspondiente al campo "Sprint" del board.** Primero obtené
   el `fieldId` del campo Sprint y las iteraciones existentes:

   ```bash
   gh api graphql -f query='
   {
     organization(login: "UPDS-DINAMITA") {
       projectV2(number: 4) {
         field(name: "Sprint") {
           ... on ProjectV2IterationField {
             id
             configuration { duration iterations { id title startDate } completedIterations { id title startDate } }
           }
         }
       }
     }
   }'
   ```

   Y reenviá **todas** las iteraciones (existentes + la nueva) en `updateProjectV2Field`
   — esta mutación reemplaza la lista completa, no agrega una sola:

   ```bash
   gh api graphql -f query='
   mutation {
     updateProjectV2Field(input: {
       fieldId: "<FIELD_ID>"
       iterationConfiguration: {
         duration: 14
         startDate: "<fecha de inicio del primer sprint, no cambia>"
         iterations: [
           { title: "Sprint 1", startDate: "2026-08-25", duration: 14 }
           { title: "Sprint 2", startDate: "2026-09-08", duration: 14 }
           { title: "Sprint 3", startDate: "2026-09-22", duration: 14 }
         ]
       }
     }) { projectV2Field { id } }
   }'
   ```

3. **Crear las issues del sprint** con sus 3 labels y el milestone:

   ```bash
   gh issue create -R Angellec21/santa-cruz-segura \
     --title "<título de la historia/tarea>" \
     --body "<qué incluye>" \
     --label "type:story,priority:high,area:backend" \
     --milestone "Sprint 3 - <objetivo del sprint>"
   ```

4. **Agregarlas al board y setear Status/Sprint.** Agregar cada issue:

   ```bash
   gh project item-add 4 --owner UPDS-DINAMITA \
     --url https://github.com/Angellec21/santa-cruz-segura/issues/<N> --format json --jq '.id'
   ```

   Con el `itemId` devuelto, el `projectId` (`PVT_kwDOE1_JUs4Bi456`), el `fieldId` de
   Status/Sprint y el id de la opción/iteración correspondiente:

   ```bash
   gh project item-edit --id <ITEM_ID> --project-id PVT_kwDOE1_JUs4Bi456 \
     --field-id <STATUS_FIELD_ID> --single-select-option-id <OPTION_ID>

   gh project item-edit --id <ITEM_ID> --project-id PVT_kwDOE1_JUs4Bi456 \
     --field-id <SPRINT_FIELD_ID> --iteration-id <ITERATION_ID>
   ```

   (Los ids de campos/opciones se obtienen una sola vez con
   `gh project field-list 4 --owner UPDS-DINAMITA --format json` y quedan fijos.)

---

## Cómo cerrar un sprint

1. Cerrar las issues que sí se completaron:

   ```bash
   gh issue close <N> -R Angellec21/santa-cruz-segura --reason completed
   ```

2. Actualizar su Status en el board a `Terminado` (ver paso 4 de la sección anterior,
   usando el option id de `Terminado`).

3. Cerrar el milestone del sprint:

   ```bash
   gh api repos/Angellec21/santa-cruz-segura/milestones/<NUMERO> -X PATCH -f state="closed"
   ```

4. Las issues que no se llegaron a completar se re-asignan al milestone del siguiente
   sprint (`gh issue edit <N> --milestone "Sprint N+1 - ..."`) y su Sprint en el board se
   mueve a la iteración nueva.

---

## Comandos de referencia rápida

```bash
# Ver issues abiertas de un sprint
gh issue list -R Angellec21/santa-cruz-segura --milestone "Sprint 2 - Hardening, integraciones reales y calidad"

# Ver todas las issues por label
gh issue list -R Angellec21/santa-cruz-segura --label "priority:critical"

# Ver campos del board (para obtener field ids / option ids)
gh project field-list 4 --owner UPDS-DINAMITA --format json

# Ver items del board con su Status y Sprint
gh project item-list 4 --owner UPDS-DINAMITA --format json

# Abrir el board en el navegador
gh project view 4 --owner UPDS-DINAMITA --web
```

---

## Notas

- El repo es público y está en la cuenta personal `Angellec21`; el Project v2 vive en la
  organización `UPDS-DINAMITA` porque GitHub Projects permite incluir issues de
  cualquier repo al que tengas acceso, sin necesidad de transferirlo.
- La protección de rama (`branch protection`) **no está activada** en este repo — no
  asumir que existe sin verificarla primero con
  `gh api repos/Angellec21/santa-cruz-segura/branches/main/protection` (aunque el repo
  es público, GitHub Free sí permite branch protection en repos públicos; en repos
  **privados** de cuentas Free, en cambio, esa protección no está disponible).
