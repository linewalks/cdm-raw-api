from main import app
import sys
if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=app.config.get("API_PORT", 5000))
