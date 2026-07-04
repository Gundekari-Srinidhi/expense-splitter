# 💰 Expense Splitter

A full-stack web application that helps users manage shared expenses with friends, roommates, or family. Users can create groups, add expenses, split bills among selected members, and view optimized settlements.

---

## 🚀 Features

- 👤 User Authentication
  - Sign Up
  - Login
  - Logout
  - Session Management

- 👥 Group Management
  - Create Group
  - Edit Group
  - Delete Group
  - Automatically adds the logged-in user as a group member

- 💸 Expense Management
  - Add Expense
  - Delete Expense
  - Split expenses among selected members
  - Track who paid

- 📊 Settlement
  - Automatic balance calculation
  - Optimized settlement suggestions
  - Mark group as settled

- 🔍 Dashboard
  - User-specific groups
  - Total Groups
  - Total Expenses
  - Total Amount
  - Search Groups
  - Sort Groups

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Flask (Python)

### Database
- MySQL

---

## 📂 Project Structure

```
ExpenseSplitter/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ExpenseSplitter.git
```

Move into the project

```bash
cd ExpenseSplitter
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

## 🗄 Database

Create a MySQL database named:

```sql
expense_splitter
```

Import the required tables and update your MySQL credentials inside `app.py`.

---

## 📸 Screenshots

(Add screenshots after deployment)

- Login Page
- Dashboard
- Create Group
- Group Details
- Add Expense
- Settlement Page

---

## 🌱 Future Improvements

- Google OAuth Login
- Forgot Password
- Edit Expense
- Email Verification
- Profile Management
- Payment Integration (UPI)

---

## 👨‍💻 Author

**G. Srinidhi**

Aspiring Full Stack Developer