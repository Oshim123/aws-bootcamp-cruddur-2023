# Week 2 — Distributed Tracing

# Week 2 — Observability

## ✅ Compulsory Tasks Completed
- Instrumented backend Flask app with **OpenTelemetry (OTEL)** and **Honeycomb.io** as the trace provider  
- Verified spans exporting to **Honeycomb dataset (backend-flask)**  
- Integrated **AWS X-Ray** into backend Flask app for distributed tracing  
- Configured and provisioned the **X-Ray daemon** in `docker-compose` to send trace data to AWS  
- Observed traces successfully in the **AWS X-Ray console**  
- Integrated **Rollbar** for error logging in the Flask backend  
- Triggered test error → verified it appeared in **Rollbar dashboard**  
- Installed **WatchTower logger** → logs now stream to **CloudWatch Log Group `cruddur`**

---

## 📚 Homework Challenges
- ✅ Add custom instrumentation to Honeycomb (**UserId, custom span**)  
  - Added a span to `/api/activities/home` with attributes: `user.handle`, `route`, `result.count`  
  - Verified attributes appear in Honeycomb events with custom span name  

- ✅ Run custom queries in Honeycomb and save them  
  - Saved **Latency by User** (`AVG(duration_ms)` grouped by `user.handle`)  
  - Saved **Recent Traces by Route** (`COUNT` grouped by `http.route`)  


---

## 💡 Reflection
- **Hardest part:** Getting traces to appear in Honeycomb (env var issue).  
- **New concept learned:** Saving queries (e.g., *Latency by User*) made performance data much easier to read.  
- **Next step:** Try grouping queries by routes and compare Honeycomb with AWS X-Ray for a fuller view.  
