# Vehicle-Parking-app-v1.0
MAD 2 Project - June 2025 - It is a multi-user app (one requires an administrator and other users) that manages different parking lots, parking spots and parked vehicles. Assume that this parking app is for 4-wheeler parking.


## Backend Setup

---

### Flask

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:

   ```bash
   python app.py
   ```

5. Stopping the Server

    * To stop the server:
    `Ctrl + C`

    * To deactivate the virtual environment:

    ```bash
    deactivate
    ```

--- 
   
---

### Redis

**Windows:**

1. Download Redis from [https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases) and extract it.

2. Navigate to the Redis folder and run the server:

   ```bash
   redis-server.exe
   ```



---

### Celery

1. Go to backend folder and launch virtual environment

2. For celery worker run this in the terminal

3. ```bash
    celery -A celery_app.celery worker --loglevel=info --pool=solo
    ```

4. For celery beat this in another terminal

    ```bash
    celery -A celery_app.celery beat --loglevel=info
    ```

---

### Mailhog

1. Download Mailhog from https://github.com/mailhog/MailHog/releases.

2. Extract and ruthe application


---

## Frontend Setup

1. Navigate to the `frontend` directory:

   ```bash
   cd frontend
   ```

2. install node modules:

   ```bash
   npm install
   ```

3. run the vue app:

   ```bash
   npm run dev
   ```

---
