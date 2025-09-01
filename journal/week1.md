# Week 1 — App Containerization

## ✅ Compulsory Tasks Completed  
- Created and worked in a Gitpod repo for Cruddur  
- Configured `.gitpod.yml` (installed Postgres client, extensions, etc.)  
- Cloned and explored frontend (`React`) and backend (`Flask`) repos  
- Got both apps running locally in containers  
- Wrote Dockerfiles for frontend and backend  
- Created a `docker-compose.yml` file to run multiple containers together  
- Mounted directories so changes update live inside containers  

## 📚 Homework Challenges  
- ✅ **Push and tag a Docker image to DockerHub**  
  - Built frontend image, tagged, and pushed successfully under `osh1m/cruddur-frontend`  
- ✅ **Use a multi-stage Dockerfile build**  
  - Tested 2-stage build for frontend → production served with `serve`  
  - Reverted back to dev-friendly Dockerfile after confirming it worked  
- ✅ **Run Dockerfile CMD as an external script**  
  - Moved `npm start` command to `start.sh` script and updated Dockerfile to call the script  

## 💡 Reflection  
- **Hardest part:** Debugging missing frontend messages when running the multi-stage build (learned this was due to dev vs prod differences).  
- **New concept learned:** How to push Docker images to DockerHub and why multi-stage builds create smaller, cleaner images.  
- **Improvement for next week:** Understand more deeply how backend and frontend containers talk to each other so I don’t get stuck on “blank UI” issues.  

