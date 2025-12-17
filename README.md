# SkillIssue1 🧠

A Python project demonstrating a simple skill-based application.  
This repo contains the main application code, a `.env` example, and required dependencies.

## 📁 Repository Structure

SkillIssue1/  
├── app/ # Application logic and modules  
├── .env.example # Example environment variables  
├── .gitignore # Files/paths ignored by Git  
├── main.py # Entry point for the application  
├── requirements.txt # Python dependencies  


## 🚀 Project Description
The project aims to provide a peer-peer learning and collaboration platoform for the students.  
The users have to provide their interests, skills and requirements to us, and we will recommend them like minded and folks with similar interests to collaborate with and to learn from.  
The UI of this application is interactive and fun to use(Tinder like).  
The recommendations are provided using vector database(Qdrant) taking the parameters like user's interests, skills, projects and recent searches.  

## 🛠️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/iamRUDRAKSH/SkillIssue1.git
   cd SkillIssue1
   ```
2. **Create & activate a virtual environment**  
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**
Copy the example:  
```bash
cp .env.example .env
```
Edit .env with your values.  
5. **Run the application**
```bash
python main.py
```
## 🤝 Contributing

1. Fork the repository  
2. Create a new branch (git checkout -b feature/awesome)  
3. Commit your changes  
4. Push to your fork  
5. Open a Pull Request  
Please follow code style and include tests where applicable.  
