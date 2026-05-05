import uvicorn
from api.main import app

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 多Agent协同运营系统启动中...")
    print("=" * 50)
    print("📍 API地址: http://localhost:8000")
    print("📍 Web界面: http://localhost:8000/web")
    print("📍 API文档: http://localhost:8000/docs")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8000)
