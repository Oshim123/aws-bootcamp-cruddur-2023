# Week 3 — Decentralised Authentication

---

## ✅ Core Tasks Done

- Set up **Amazon Cognito** to handle sign-in / sign-up  
- Hooked up the **React frontend** to Cognito using **Amplify v6**  
- Backend (Flask) now checks JWT tokens on every request  
- Pulled public keys from the **Cognito JWKS endpoint** to verify tokens  
- Validated the usual stuff:
  - `iss` (issuer URL)
  - `aud` (client ID / audience)
  - `exp` (expiry time)  
- Updated CORS settings so it allows `"Content-Type"`, `"Authorization"` and `"X-Requested-With"` headers  
- Tested everything with curl:
  - ✅ Valid token = 200 OK  
  - ❌ Expired/invalid token = 401 error as expected  

---

## 📚 Extra Challenges

- ✅ Manually verified JWTs using `PyJWT` and `jose` libs (just to know what’s going on under the hood)    
- ✅ Learned the difference between:
  - `id_token` = user info  
  - `access_token` = for hitting APIs  
  - `refresh_token` = to stay logged in   

---

## 💬 Thoughts

- **Trickiest bit:** Getting my head around how the key verification works (JWKS)  
- **Most useful thing I learned:** Backend doesn’t need to call Cognito every time — token handles that, so it’s proper scalable  
- **Next step:** Add logic to the frontend so it only shows content if you’re logged in  

---

## 🔑 Key Points to Remember

- Cognito does identity the modern (decentralised) way — no need to store passwords yourself  
- Backend checks:
  - ✅ Signature via public key  
  - ✅ Right issuer  
  - ✅ Right audience (client ID)  
  - ✅ Token not expired  
- Don’t ever leave tokens lying around in the browser — memory is safer  
- This whole setup means you can build secure apps that scale without managing your own login system  

---
