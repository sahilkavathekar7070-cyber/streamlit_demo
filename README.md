# streamlit_demo
# 🚆 Railway Reservation System

A professional **Railway Reservation Management System** developed using **Python, Streamlit, and SQLite3**.

The application allows users to book railway tickets, automatically calculate fares, allocate seats, generate unique PNR numbers, search existing bookings, cancel tickets, and retrieve booking records from a persistent SQLite database.

---

## 📌 Project Overview

The Railway Reservation System provides a simple and user-friendly web interface for managing railway reservations.

Users can:

* Select a train
* Select journey date
* Select travel class
* Enter passenger details
* Select the number of seats
* Calculate the fare automatically
* Generate a unique PNR number
* Store booking information in SQLite3
* Search bookings using PNR
* Cancel confirmed bookings
* Restore cancelled seats automatically
* View all booking records
* Download booking records as CSV

The project demonstrates how a **Python-based frontend can be connected to a relational SQLite database** to create a complete database-driven application.

---

## ✨ Features

### 🎫 Ticket Booking

* Train selection
* Journey date selection
* Travel class selection
* Passenger information form
* Mobile number validation
* Email validation
* Number of seats selection
* Automatic seat availability checking
* Automatic fare calculation
* Automatic seat allocation
* Unique PNR generation

### 🔎 Booking Search

Users can search their booking using a **10-digit PNR number**.

The application displays:

* PNR
* Passenger name
* Age
* Gender
* Phone number
* Email
* Train details
* Source
* Destination
* Journey date
* Class
* Seat numbers
* Total fare
* Booking status
* Booking time

### ❌ Ticket Cancellation

Users can:

* Search a booking using PNR
* View booking information
* Confirm cancellation
* Cancel the ticket
* Automatically restore the cancelled seats
* Update booking status to `CANCELLED`

### 📋 Booking Management

The application provides an administration-style booking table containing:

* PNR
* Passenger
* Train
* Source
* Destination
* Journey date
* Class
* Seats
* Fare
* Status
* Booking time

Booking records can also be exported as a CSV file.

---

# 🏗️ System Architecture

```text
                ┌───────────────────────────┐
                │      Streamlit UI         │
                │                           │
                │  Booking / Search /       │
                │  Cancellation / Records   │
                └─────────────┬─────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │       Python Logic        │
                │                           │
                │ Validation                │
                │ Fare Calculation          │
                │ PNR Generation            │
                │ Seat Allocation           │
                │ Booking Management        │
                └─────────────┬─────────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │         SQLite3           │
                │                           │
                │  trains                   │
                │  train_seats              │
                │  bookings                 │
                └───────────────────────────┘
```

---

# 🗄️ Database Design

The project uses **SQLite3** as its database.

The database file is automatically created as:

```text
railway.db
```

## 1. `trains` Table

Stores train information.

| Column           | Description         |
| ---------------- | ------------------- |
| `train_id`       | Unique train ID     |
| `train_number`   | Train number        |
| `train_name`     | Train name          |
| `source`         | Starting station    |
| `destination`    | Destination station |
| `departure_time` | Departure time      |
| `arrival_time`   | Arrival time        |
| `duration`       | Journey duration    |

---

## 2. `train_seats` Table

Stores class-wise and date-wise seat availability.

| Column            | Description               |
| ----------------- | ------------------------- |
| `seat_id`         | Unique seat record        |
| `train_id`        | Associated train          |
| `travel_date`     | Journey date              |
| `class_type`      | Travel class              |
| `total_seats`     | Total seats               |
| `available_seats` | Currently available seats |

A unique constraint is maintained for:

```text
train_id + travel_date + class_type
```

This prevents duplicate seat records for the same train, date and class.

---

## 3. `bookings` Table

Stores passenger reservation details.

| Column           | Description         |
| ---------------- | ------------------- |
| `booking_id`     | Unique booking ID   |
| `pnr`            | Unique PNR number   |
| `train_id`       | Associated train    |
| `passenger_name` | Passenger name      |
| `age`            | Passenger age       |
| `gender`         | Passenger gender    |
| `phone`          | Mobile number       |
| `email`          | Email address       |
| `source`         | Starting station    |
| `destination`    | Destination         |
| `journey_date`   | Journey date        |
| `class_type`     | Travel class        |
| `seat_count`     | Number of seats     |
| `seat_numbers`   | Allocated seats     |
| `fare_per_seat`  | Fare per seat       |
| `total_fare`     | Total booking fare  |
| `booking_status` | CONFIRMED/CANCELLED |
| `booking_time`   | Booking timestamp   |

---

# 🚆 Available Travel Classes

The application currently supports:

| Class               | Example Fare |
| ------------------- | -----------: |
| Sleeper (SL)        |         ₹500 |
| AC 3 Tier (3A)      |       ₹1,200 |
| AC 2 Tier (2A)      |       ₹1,800 |
| AC First Class (1A) |       ₹2,500 |
| Chair Car (CC)      |         ₹800 |

> These fares are configured for project/demo purposes and can be modified in the Python code.

---

# 🚆 Sample Trains

The application is initialized with sample train data such as:

| Train No. | Train              | Source         | Destination |
| --------- | ------------------ | -------------- | ----------- |
| 12951     | Mumbai Rajdhani    | Mumbai Central | New Delhi   |
| 12009     | Mumbai Shatabdi    | Mumbai Central | Ahmedabad   |
| 12109     | Panchavati Express | Mumbai CSMT    | Manmad      |
| 11010     | Sinhagad Express   | Pune           | Mumbai CSMT |
| 12124     | Deccan Queen       | Pune           | Mumbai CSMT |

These are included as **sample/project data** and are not intended to represent live railway schedules.

---

# 📁 Project Structure

```text
Railway_Reservation/
│
├── app.py
├── railway.db
├── requirements.txt
└── README.md
```

### `app.py`

Main Streamlit application containing:

* User interface
* Database operations
* Booking logic
* Seat management
* Fare calculation
* PNR generation
* Search functionality
* Cancellation functionality

### `railway.db`

SQLite database created automatically when the application is executed.

### `requirements.txt`

Contains Python dependencies required to run the project.

### `README.md`

Project documentation.

---

# 💻 Technologies Used

## Programming Language

**Python**

## Frontend

**Streamlit**

Streamlit is used to create the interactive web-based user interface.

## Database

**SQLite3**

SQLite is used for persistent storage of:

* Train data
* Seat availability
* Passenger information
* Booking information

## Libraries

```text
streamlit
pandas
sqlite3
datetime
random
string
```

`sqlite3`, `datetime`, `random`, and `string` are part of Python's standard library.

---

# ⚙️ Installation

## Step 1: Clone or Download the Project

Download the project to your computer.

Open the project directory:

```bash
cd Railway_Reservation
```

---

## Step 2: Create a Virtual Environment

Optional but recommended:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## Step 3: Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Run the following command:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL, normally similar to:

```text
http://localhost:8501
```

Open the displayed address in your browser.

---

# 🔄 Application Workflow

## Step 1 — Select Train

Select a train from the available train list.

The application displays:

* Train number
* Train name
* Source
* Destination
* Departure
* Arrival

---

## Step 2 — Select Journey Details

Enter:

```text
Journey Date
Travel Class
Number of Seats
```

The system checks the available seats for the selected train, date and class.

---

## Step 3 — Enter Passenger Details

Enter:

```text
Passenger Name
Age
Gender
Mobile Number
Email
```

---

## Step 4 — Calculate Fare

The application calculates:

```text
Total Fare =
Fare Per Seat × Number of Seats
```

For example:

```text
Fare per seat = ₹1,200
Number of seats = 2

Total Fare = ₹1,200 × 2

Total Fare = ₹2,400
```

---

## Step 5 — Confirm Booking

After successful validation:

1. Availability is checked.
2. Seats are allocated.
3. A unique PNR is generated.
4. Booking information is inserted into SQLite.
5. Available seat count is reduced.
6. Booking confirmation is displayed.

---

# 🔐 Transaction Management

The booking and cancellation operations use SQLite transactions.

For example:

```python
conn.execute("BEGIN IMMEDIATE")
```

If all operations succeed:

```python
conn.commit()
```

If an error occurs:

```python
conn.rollback()
```

This helps prevent partially completed booking operations.

For example, a booking should not be stored while the seat count remains unchanged.

---

# 🪑 Seat Management

The application automatically maintains seat availability.

Example:

```text
Initial Available Seats = 64

Passenger books 3 seats

Available Seats = 61
```

After cancellation:

```text
Available Seats = 64
```

The system also checks previously allocated seats before assigning new seats.

---

# 🔎 PNR Search

Each booking receives a unique 10-digit PNR.

Example:

```text
5839271046
```

The PNR can be used to retrieve the booking details from the SQLite database.

---

# ❌ Cancellation Workflow

The cancellation process is:

```text
Enter PNR
     ↓
Find Booking
     ↓
Display Booking
     ↓
Confirm Cancellation
     ↓
Update Status
     ↓
Restore Seats
```

The booking status changes from:

```text
CONFIRMED
```

to:

```text
CANCELLED
```

The booking record is retained rather than deleted, which preserves the booking history.

---

# 📊 Dashboard

The dashboard displays summary information such as:

* Total bookings
* Confirmed bookings
* Cancelled bookings
* Revenue from confirmed bookings

This provides a quick overview of the reservation database.

---

# 📥 Export Booking Data

The **All Bookings** page allows booking records to be downloaded as:

```text
railway_bookings.csv
```

This can be opened using:

* Microsoft Excel
* Google Sheets
* Python Pandas
* Other spreadsheet applications

---

# 🧪 Validation

The application performs basic validation for:

### Passenger Name

Cannot be empty.

### Mobile Number

Must contain exactly 10 digits.

### Email

If provided, it must contain `@`.

### PNR

Must contain exactly 10 digits.

### Seats

Cannot exceed currently available seats.

---

# 🔒 Data Integrity

The application uses:

* Primary keys
* Unique constraints
* Foreign keys
* SQLite transactions
* Booking status
* Seat availability tracking

These mechanisms help maintain consistency between bookings and seat availability.

---

# 🎯 Project Objectives

The main objectives of the project are:

1. To develop a simple railway reservation interface.
2. To automate the ticket booking process.
3. To store passenger and booking information digitally.
4. To maintain seat availability.
5. To automatically calculate ticket fares.
6. To generate unique PNR numbers.
7. To provide booking search functionality.
8. To provide ticket cancellation functionality.
9. To demonstrate database connectivity using SQLite3.
10. To provide a practical Python + Streamlit project.

---

# 🌟 Advantages

* Simple and user-friendly interface
* Fast booking process
* Persistent database storage
* Automatic fare calculation
* Automatic seat allocation
* PNR-based booking retrieval
* Cancellation support
* Seat restoration after cancellation
* CSV export
* Lightweight SQLite database
* No separate database server required

---

# ⚠️ Limitations

This project is intended as an educational/project implementation and does not connect to a live railway reservation service.

Current limitations include:

* No live train availability
* No real payment gateway
* No railway API integration
* Sample train data
* Basic authentication
* Single-passenger booking form
* No real railway ticket generation
* No SMS/email notification service

---

# 🚀 Future Enhancements

The system can be extended with:

### 👤 User Authentication

* User registration
* Login/logout
* Password hashing
* User profiles

### 👨‍💼 Admin Panel

* Add trains
* Update trains
* Delete trains
* Manage fares
* View passenger records
* Manage seat capacity

### 🎫 Advanced Ticketing

* Multiple passengers under one PNR
* Coach selection
* Berth preference
* Automatic berth allocation
* Waiting-list management
* RAC support

### 💳 Payment Integration

A payment gateway can be integrated for online payments.

### 📄 PDF Ticket

Generate a professional railway ticket PDF containing:

```text
PNR
Passenger
Train
Journey
Coach
Seat
Fare
Booking Status
```

### 📧 Notifications

Add:

* Email confirmation
* SMS notification
* Cancellation notification

### 📊 Analytics

Add charts for:

* Daily bookings
* Revenue
* Popular trains
* Class-wise bookings
* Cancellation rate
* Seat utilization

### 🌐 Deployment

The application can be deployed using a suitable cloud hosting platform supporting Streamlit applications.

---

# 🛠️ Troubleshooting

## Streamlit command not found

Try:

```bash
python -m streamlit run app.py
```

---

## ModuleNotFoundError

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Database issues

The application automatically creates:

```text
railway.db
```

If you are starting a completely fresh project database, stop the Streamlit application, remove `railway.db`, and run the application again.

> Removing the database permanently removes all locally stored booking records.

---

# 📚 Learning Outcomes

This project provides practical experience with:

* Python programming
* Streamlit
* SQLite3
* SQL queries
* CRUD operations
* Database relationships
* Transactions
* Form handling
* Input validation
* Session state
* Data processing with Pandas
* CSV export
* Frontend styling
* Application architecture

---

# 👩‍💻 Author

**Vaishnavi Kumavat**

### Technologies

```text
Python
Streamlit
SQLite3
Pandas
SQL
```

---

# 📜 License

This project is developed for **educational and academic purposes**.

You may modify and extend the project according to your requirements.

---

## ⭐ Conclusion

The Railway Reservation System demonstrates how **Python, Streamlit and SQLite3** can be combined to build a functional database-driven web application.

The system provides an end-to-end reservation workflow:

```text
Passenger Details
       ↓
Train Selection
       ↓
Journey Details
       ↓
Seat Availability
       ↓
Fare Calculation
       ↓
PNR Generation
       ↓
SQLite Database
       ↓
Search / Cancellation / Reporting
```

The project can serve as a foundation for developing a more advanced railway reservation platform with authentication, payment integration, PDF ticket generation, multiple passengers, live train APIs and advanced analytics.
