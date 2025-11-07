## 1. Create virtual env and install
```
C:\Users\<name>\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

Requirements.txt should at minimum should have:
```
flask==3.1.2
flask-cors==6.0.1
```

### 1.1 Add .gitignore
To not commit unnecessary files

## 2. Backend from scratch
Create a folder api and create index.py with the following code:
```
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# While testing, allow both your frontend domain(s)
CORS(app, origins=[
    "https://richwellp.github.io"
])

@app.get("/")
def root():
    return jsonify(message="Hello from Flask on Vercel!")
```

## 3. Vercel Deployment
Create a vercel file:
```
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    { "source": "/", "destination": "/api" }, 
    { "source": "/(.*)", "destination": "/api/$1" } 
  ]
}
```
The first rewrite maps the root to /api/index.py
The second rewrite maps all to /api/<"path">


## 4. Point the frontend to the deployed backend

```
VITE_API_BASE=https://<your-app>.vercel.app
```

Create a tiny client and call it ```frontend/src/api.ts```:

```
export const API = import.meta.env.VITE_API_BASE;

export async function hello() {
  const r = await fetch(`${API}/hello`); // or `${API}/` if your root returns JSON
  if (!r.ok) throw new Error(`API ${r.status}`);
  return r.json();
}
```
Example use (in a component):
```
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { hello } from './api'
const msg = ref('...')
onMounted(async () => { msg.value = (await hello()).message })
</script>

<template><p>{{ msg }}</p></template>
```

## 5. Deploy the frontend (Github pages)
Make sure your workflow builds from /frontend:
```
# .github/workflows/deploy.yml
- name: Install
  run: cd frontend && npm install
- name: Build
  run: cd frontend && npm run build
- name: Upload artifact
  uses: actions/upload-pages-artifact@v4
  with: { path: frontend/dist }
```

Repo is public, Settings → Pages → Source: GitHub Actions.
Push a commit → wait for the Action to turn green → open: https://richwellp.github.io

## 6. Prod hardening (optional)
Add health endpoint:
```
@app.get("/healthz")
def healthz(): return {"ok": True}
```


