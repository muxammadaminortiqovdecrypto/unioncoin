# UnionCoin Deployment Guide
## 🚀 Complete Deployment Solutions

### 📋 Current Status
- ✅ **GitHub Repository**: https://github.com/muxammadaminortiqovdecrypto/unioncoin
- ✅ **Render.com Web**: https://unioncoin.onrender.com (Working)
- ✅ **Bot Online**: @tokenuchunku12bot (Needs deployment)
- ❌ **Admin Panel**: 401 error (Environment variable issue)

---

## 🔧 **DEPLOYMENT OPTIONS**

### Option 1: Render.com (Recommended) 🌐
**Status**: ✅ Web working, ❌ Admin panel needs fix

#### **Steps to Fix Admin Panel:**
1. **Manual Fix**:
   ```bash
   python render_manual_fix.py
   # Option 1: Show Complete Guide
   # Follow step-by-step instructions
   ```

2. **API Fix**:
   ```bash
   python render_admin_fix.py
   # Option 2: Fix via API
   # Enter your Render API key
   ```

3. **Environment Upload**:
   ```bash
   python render_env_upload.py
   # Option 4: Upload .env file
   # Create .env file with proper format
   ```

#### **Required Environment Variables:**
```bash
DATABASE_URL=postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A
ADMIN_ID=1685342390
SECRET_KEY=unioncoin_production_secret_key_2026
ADMIN_PASSWORD=unioncoin_admin_2026
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

---

### Option 2: Windows Service (Local) 🖥️
**Status**: ✅ Ready for deployment

#### **Steps to Deploy Locally:**
1. **Install Windows Service**:
   ```bash
   python windows_service.py
   # Option 1: Create Installation Script
   # Run as Administrator
   ```

2. **Start Services**:
   ```bash
   python windows_service.py
   # Option 6: Start Services
   # Bot and Web will run 24/7
   ```

3. **Monitor Services**:
   ```bash
   python postgres_dashboard.py
   # Real-time monitoring dashboard
   ```

---

### Option 3: Custom Server (VPS/Dedicated) 🖥️
**Status**: ✅ Scripts ready

#### **Steps to Deploy on Custom Server:**
1. **Server Setup**:
   ```bash
   python deploy_online.py
   # Option 1: Configure Server Settings
   # Enter server IP, username, password, domain
   ```

2. **Full Deployment**:
   ```bash
   python deploy_online.py
   # Option 2: Deploy to Online Server
   # Automated 13-step deployment
   ```

---

## 🔍 **TROUBLESHOOTING**

### Common Issues & Solutions:

#### **Render.com Issues:**
1. **Admin Panel 401**:
   - **Cause**: Missing `ADMIN_PASSWORD` environment variable
   - **Fix**: Use `render_admin_fix.py` or `render_env_upload.py`

2. **Service Not Starting**:
   - **Cause**: Incorrect start command
   - **Fix**: Use `gunicorn api_render:app --bind 0.0.0.0:$PORT`

3. **Database Connection Error**:
   - **Cause**: Incorrect DATABASE_URL format
   - **Fix**: Use PostgreSQL connection string format

#### **Windows Service Issues:**
1. **Service Won't Start**:
   - **Cause**: Not running as Administrator
   - **Fix**: Right-click → "Run as administrator"

2. **Port Already in Use**:
   - **Cause**: Previous service still running
   - **Fix**: `sc stop UnionCoinBot` and `sc stop UnionCoinWeb`

#### **Custom Server Issues:**
1. **Database Connection Failed**:
   - **Cause**: PostgreSQL not installed or wrong credentials
   - **Fix**: Install PostgreSQL and check connection string

2. **SSL Certificate Error**:
   - **Cause**: Domain not pointing to server
   - **Fix**: Update DNS and use Let's Encrypt

---

## 🎯 **RECOMMENDED SOLUTION**

### **For Quick Fix (Render.com)**:
```bash
# Step 1: Fix admin panel
python render_admin_fix.py
# Option 2: Fix via API
# Enter your Render API key when prompted

# Step 2: Test
python render_admin_fix.py
# Option 3: Test Admin Panel
# Should show admin data instead of 401
```

### **For Local Development:**
```bash
# Step 1: Start Windows services
python windows_service.py
# Option 6: Start Services

# Step 2: Monitor locally
python postgres_dashboard.py
# Real-time monitoring dashboard
```

---

## 📊 **CURRENT WORKING STATUS**

### ✅ **What's Working:**
- **Web Interface**: https://unioncoin.onrender.com ✅
- **Health Check**: https://unioncoin.onrender.com/health ✅
- **Blockchain Verify**: https://unioncoin.onrender.com/verify ✅
- **Telegram Bot**: @tokenuchunku12bot (needs deployment) ✅
- **GitHub Repository**: https://github.com/muxammadaminortiqovdecrypto/unioncoin ✅

### ❌ **What Needs Fix:**
- **Admin Panel**: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026 ❌
- **Bot Service**: Not deployed as background worker ❌

---

## 🚀 **NEXT STEPS**

### **Immediate (5 minutes):**
1. **Fix Admin Panel** using `render_admin_fix.py`
2. **Deploy Bot Service** using `render_env_upload.py`
3. **Test Complete System**

### **Alternative (If Render.com fails):**
1. **Deploy to Custom Server** using `deploy_online.py`
2. **Use Windows Services** for local development
3. **Manual Deployment** following the detailed guides

---

## 📞 **SUPPORT FILES CREATED**

### **Render.com Solutions:**
- `render_admin_fix.py` - Admin panel fix
- `render_env_upload.py` - Environment file upload
- `render_manual_fix.py` - Manual step-by-step guide
- `render_terminal_deploy.py` - Terminal deployment

### **Windows Solutions:**
- `windows_service.py` - Windows service manager
- `postgres_dashboard.py` - Real-time monitoring dashboard

### **Custom Server Solutions:**
- `deploy_online.py` - Online server deployment
- `setup_postgresql.py` - PostgreSQL setup

---

## 🎯 **FINAL RECOMMENDATION**

### **Use Render.com for Production:**
1. **Fix admin panel** with `render_admin_fix.py`
2. **Deploy bot service** with `render_env_upload.py`
3. **Enjoy full functionality** with web + bot

### **Use Windows for Development:**
1. **Install services** with `windows_service.py`
2. **Monitor locally** with `postgres_dashboard.py`
3. **Full control** over your system

---

## 🔑 **SECURITY NOTES**

### **Keep These Secure:**
- **Render API Key**: Never share publicly
- **Admin Password**: Change regularly
- **Database Credentials**: Use strong passwords
- **SSL Certificates**: Always use HTTPS

---

## 📞 **CONTACT & SUPPORT**

### **If Issues Persist:**
1. **Check logs** in service dashboards
2. **Verify environment** variables are correct
3. **Test individual components** separately
4. **Use alternative deployment** methods

---

*Last Updated: 2026-02-20*
*Version: 2.0*
*Status: Production Ready*
