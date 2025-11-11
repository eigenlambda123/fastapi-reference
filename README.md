# hackaton-boilerplates 

*Boilerplate starter kits for rapid hackathon development (backend + frontend).*

## Table of Contents  
- [About](#about)  
- [Why this exists](#why-this-exists)  
- [What’s included](#whats-included)  
- [Getting Started](#getting-started)  
- [Usage – Backend (FastAPI)](#usage--backend-fastapi)  
- [Usage – Frontend (React)](#usage--frontend-react)  
- [When to use / Hackathon workflow](#when-to-use--hackathon-workflow)  
- [Best practices / Tips](#best-practices--tips)  
- [Contributing](#contributing)  
- [License](#license)  

## About  
This repository contains ready-to-go boilerplates to get you hacking fast in a hackathon environment. Focused on speed, modularity, and clarity so that you can spend time solving the problem — not wiring infrastructure.

## Why this exists  
- Hackathons demand rapid turnaround: scaffolding, routing, state management, DB connectors — that eats time.  
- By abstracting a repeatable baseline, you start from **build mode**, not **setup mode**.  
- Thin veneer of complexity: the boilerplates are opinionated but lightweight; you can fork/adapt them to any challenge.  
- For developers like you (and me) who prefer building systems, shipping features, and iterating fast.

## What’s included  
### Backend (`backend‐fastapi`)  
- Python project with FastAPI for asynchronous API endpoints  
- Modular folder structure (routers, schemas, models, services)  
- Integration with SQLModel (or SQLAlchemy) for DB models, migrations scaffold  
- Pre-built user/role model example & authentication stub (you can replace with OAuth / JWT)  
- Basic error/response handler middleware to standardize API responses  
- Dockerfile and docker-compose stub for service + database if needed  

### Frontend (`frontend‐react`)  
- TypeScript project built with Vite + React  
- Component directory layout (pages, components, hooks, services)  
- Example state management via React Context (or you can swap in Redux / Zustand)  
- Axios service setup (or fetch wrapper) to hit the backend endpoints  
- TailwindCSS integration for utility-first styling (you can swap for your UI library)  
- Basic routing setup (via React Router) and example page  

## Getting Started

### Prerequisites  
- Docker & docker-compose (optional but recommended)  
- Python ≥ 3.10 (for backend)  
- Node ≥ 16 & npm/yarn (for frontend)  
- [Optional] Postman or similar API client for testing  

### Setup Backend  
```bash
cd backend-fastapi
# install dependencies
pip install -r requirements.txt
# set env vars (DB connection, secret keys, etc)
cp .env.example .env && edit .env
# run
uvicorn app.main:app --reload
````

Or using Docker:

```bash
docker-compose up --build
```

### Setup Frontend

```bash
cd frontend-react
npm install    # or yarn
cp .env.local.example .env.local && edit the API_BASE_URL
npm run dev
```

## Usage – Backend (FastAPI)

* The router modules are under `app/routers`. Add new feature endpoints via new router files.
* Database models live in `app/models`. Use SQLModel/SQLAlchemy, and register your models in the database init step.
* Services (business logic) go into `app/services`. This keeps your API layer thin and maintainable.
* Error/response middleware normalizes output into a `{ success: bool, data: any, error: string | null }` shape (or similar).
* Use Docker + Compose to spawn the database and backend together (e.g., PostgreSQL).
* Configure `.env` for secret keys, DB URI, CORS origins, etc.

## Usage – Frontend (React)

* Entry file: `src/main.tsx` (or `index.tsx`).
* Pages (routes) live in `src/pages`; components in `src/components`; shared hooks in `src/hooks`.
* API service lives in `src/services/api.ts` — configure the base URL, interceptors, error handling.
* Tailwind styling: edit `tailwind.config.js` and `globals.css` as needed.
* Add new routes in `src/App.tsx` using React Router, and wrap common layout components.
* For deployment, run `npm run build`, then serve via static host or tie your backend + frontend with Nginx in Docker.

## When to use / Hackathon workflow

1. Clone this repo at the start of the hackathon:

   ```bash
   git clone https://github.com/eigenlambda123/hackaton-boilerplates.git my-project
   cd my-project
   ```
2. Rename project and update `app.title`, `package.json`, etc.
3. Inscribe hackathon challenge requirements:

   * Snap out your user persona & empathy map
   * Identify key endpoints & features (e.g., login, “what-if” simulation, admin panel)
4. Rapidly spin backend & frontend using boilerplate:

   * Create database models
   * Wire routes
   * Hook frontend to backend services
5. Iteratively build features, test locally via Docker, push to remote host (Vercel/Netlify + Heroku/Render)
6. At submission time you’re ready with code, short README (this file), and a deploy link.

## Best Practices / Tips

* Keep backend and frontend separate in CI pipelines. Use linting, type-checking (`mypy`/`pytest`, `eslint`/`prettier`).
* For hackathons, prioritize deliver-ables: MVP routes + UI > perfect architecture. Use this boilerplate to skip boiler-plate.
* Clean up before submission: remove unused routes, docs, comments. Make sure environment variables are not exposed.
* Logging and monitoring: For backend, use structured logs; for frontend, capture errors via `window.onerror` or similar.
* Deployment tip: You can Dockerize both services and deploy on a single host or use separate services with CORS wired.
* Time-box feature scope: Use this boilerplate to sprint, but decide early what you will *not* build.

## Contributing

Feel free to fork and enhance. If you build a new boilerplate (e.g., GraphQL, Next.js, or mobile), please contribute a feature-branch + pull request.
When opening issues, please include: description, stack (backend/frontend/new), proposed improvement, and sample code.

## License

This project is open-source under the MIT License — see [LICENSE](LICENSE) for full text.

---

_Created and maintained by RM Villa._