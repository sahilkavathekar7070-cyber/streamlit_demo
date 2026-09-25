import streamlit as st
import sqlite3
import random
import string
from datetime import datetime, date

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Railway Reservation System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main title */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Booking confirmation */
    .success-card {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .pnr {
        font-size: 28px;
        font-weight: 700;
        color: #047857;
    }

    /* Section heading */
    .section-title {
        font-size: 22px;
        font-weight: 650;
        color: #111827;
        margin-bottom: 12px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 15px;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_NAME = "railway.db"


def get_connection():
    """
    Create SQLite connection.
    """
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # TRAINS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trains (
            train_id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_number TEXT UNIQUE NOT NULL,
            train_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            duration TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # SEATS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS train_seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            travel_date TEXT NOT NULL,
            class_type TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,

            UNIQUE(train_id, travel_date, class_type),

            FOREIGN KEY(train_id)
            REFERENCES trains(train_id)
        )
    """)

    # --------------------------------------------------------
    # BOOKINGS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,

            pnr TEXT UNIQUE NOT NULL,

            train_id INTEGER NOT NULL,

            passenger_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,

            source TEXT NOT NULL,
            destination TEXT NOT NULL,

            journey_date TEXT NOT NULL,
            class_type TEXT NOT NULL,

            seat_count INTEGER NOT NULL,
            seat_numbers TEXT NOT NULL,

            fare_per_seat REAL NOT NULL,
            total_fare REAL NOT NULL,

            booking_status TEXT NOT NULL DEFAULT 'CONFIRMED',

            booking_time TEXT NOT NULL,

            FOREIGN KEY(train_id)
            REFERENCES trains(train_id)
        )
    """)

    # --------------------------------------------------------
    # INSERT SAMPLE TRAINS
    # --------------------------------------------------------

    sample_trains = [
        (
            "12951",
            "Mumbai Rajdhani",
            "Mumbai Central",
            "New Delhi",
            "17:00",
            "08:35",
            "15h 35m"
        ),
        (
            "12009",
            "Mumbai Shatabdi",
            "Mumbai Central",
            "Ahmedabad",
            "06:25",
            "13:40",
            "7h 15m"
        ),
        (
            "12109",
            "Panchavati Express",
            "Mumbai CSMT",
            "Manmad",
            "18:15",
            "22:55",
            "4h 40m"
        ),
        (
            "11010",
            "Sinhagad Express",
            "Pune",
            "Mumbai CSMT",
            "06:05",
            "09:35",
            "3h 30m"
        ),
        (
            "12124",
            "Deccan Queen",
            "Pune",
            "Mumbai CSMT",
            "07:15",
            "10:25",
            "3h 10m"
        )
    ]

    for train in sample_trains:

        cursor.execute("""
            INSERT OR IGNORE INTO trains
            (
                train_number,
                train_name,
                source,
                destination,
                departure_time,
                arrival_time,
                duration
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, train)

    conn.commit()
    conn.close()


initialize_database()


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_pnr():
    """
    Generate unique 10-digit PNR.
    """

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        pnr = ''.join(
            random.choices(
                string.digits,
                k=10
            )
        )

        cursor.execute(
            "SELECT pnr FROM bookings WHERE pnr = ?",
            (pnr,)
        )

        if cursor.fetchone() is None:
            conn.close()
            return pnr


def get_trains():
    conn = get_connection()

    trains = conn.execute("""
        SELECT *
        FROM trains
        ORDER BY train_number
    """).fetchall()

    conn.close()

    return trains


def get_train_by_id(train_id):

    conn = get_connection()

    train = conn.execute("""
        SELECT *
        FROM trains
        WHERE train_id = ?
    """, (train_id,)).fetchone()

    conn.close()

    return train


def get_fare(class_type):

    fares = {
        "Sleeper (SL)": 500,
        "AC 3 Tier (3A)": 1200,
        "AC 2 Tier (2A)": 1800,
        "AC First Class (1A)": 2500,
        "Chair Car (CC)": 800
    }

    return fares[class_type]


def initialize_seats(train_id, journey_date):

    conn = get_connection()
    cursor = conn.cursor()

    seat_config = {
        "Sleeper (SL)": 72,
        "AC 3 Tier (3A)": 64,
        "AC 2 Tier (2A)": 48,
        "AC First Class (1A)": 24,
        "Chair Car (CC)": 78
    }

    for class_type, total in seat_config.items():

        cursor.execute("""
            INSERT OR IGNORE INTO train_seats
            (
                train_id,
                travel_date,
                class_type,
                total_seats,
                available_seats
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            train_id,
            journey_date,
            class_type,
            total,
            total
        ))

    conn.commit()
    conn.close()


def get_available_seats(
    train_id,
    journey_date,
    class_type
):

    initialize_seats(
        train_id,
        journey_date
    )

    conn = get_connection()

    row = conn.execute("""
        SELECT available_seats
        FROM train_seats
        WHERE train_id = ?
        AND travel_date = ?
        AND class_type = ?
    """, (
        train_id,
        journey_date,
        class_type
    )).fetchone()

    conn.close()

    if row:
        return row["available_seats"]

    return 0


def generate_seat_numbers(
    train_id,
    journey_date,
    class_type,
    count
):

    conn = get_connection()

    # Existing booked seats
    rows = conn.execute("""
        SELECT seat_numbers
        FROM bookings
        WHERE train_id = ?
        AND journey_date = ?
        AND class_type = ?
        AND booking_status = 'CONFIRMED'
    """, (
        train_id,
        journey_date,
        class_type
    )).fetchall()

    conn.close()

    occupied = set()

    for row in rows:

        if row["seat_numbers"]:

            seats = row["seat_numbers"].split(",")

            for seat in seats:
                occupied.add(seat.strip())

    # Maximum seat number according to class
    max_seats = {
        "Sleeper (SL)": 72,
        "AC 3 Tier (3A)": 64,
        "AC 2 Tier (2A)": 48,
        "AC First Class (1A)": 24,
        "Chair Car (CC)": 78
    }[class_type]

    available = []

    for number in range(1, max_seats + 1):

        seat = f"{class_type.split()[0]}-{number}"

        if seat not in occupied:
            available.append(seat)

        if len(available) == count:
            break

    return available


def create_booking(
    train_id,
    passenger_name,
    age,
    gender,
    phone,
    email,
    source,
    destination,
    journey_date,
    class_type,
    seat_count
):

    conn = get_connection()

    try:

        # Start transaction
        conn.execute("BEGIN IMMEDIATE")

        # Make sure seat record exists
        cursor = conn.cursor()

        seat_config = {
            "Sleeper (SL)": 72,
            "AC 3 Tier (3A)": 64,
            "AC 2 Tier (2A)": 48,
            "AC First Class (1A)": 24,
            "Chair Car (CC)": 78
        }

        total_seats = seat_config[class_type]

        cursor.execute("""
            INSERT OR IGNORE INTO train_seats
            (
                train_id,
                travel_date,
                class_type,
                total_seats,
                available_seats
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            train_id,
            journey_date,
            class_type,
            total_seats,
            total_seats
        ))

        # Check availability
        row = cursor.execute("""
            SELECT available_seats
            FROM train_seats
            WHERE train_id = ?
            AND travel_date = ?
            AND class_type = ?
        """, (
            train_id,
            journey_date,
            class_type
        )).fetchone()

        available = row["available_seats"]

        if available < seat_count:

            conn.rollback()

            return None, (
                f"Only {available} seat(s) are available."
            )

        # Generate seats
        booked_rows = cursor.execute("""
            SELECT seat_numbers
            FROM bookings
            WHERE train_id = ?
            AND journey_date = ?
            AND class_type = ?
            AND booking_status = 'CONFIRMED'
        """, (
            train_id,
            journey_date,
            class_type
        )).fetchall()

        occupied = set()

        for booked_row in booked_rows:

            if booked_row["seat_numbers"]:

                for seat in booked_row["seat_numbers"].split(","):
                    occupied.add(seat.strip())

        available_seat_numbers = []

        for number in range(1, total_seats + 1):

            seat = f"{class_type.split()[0]}-{number}"

            if seat not in occupied:

                available_seat_numbers.append(seat)

            if len(available_seat_numbers) == seat_count:
                break

        if len(available_seat_numbers) < seat_count:

            conn.rollback()

            return None, "Unable to allocate seats."

        # Generate PNR
        while True:

            pnr = ''.join(
                random.choices(
                    string.digits,
                    k=10
                )
            )

            exists = cursor.execute("""
                SELECT pnr
                FROM bookings
                WHERE pnr = ?
            """, (pnr,)).fetchone()

            if exists is None:
                break

        fare_per_seat = get_fare(class_type)

        total_fare = fare_per_seat * seat_count

        seat_numbers = ",".join(
            available_seat_numbers
        )

        booking_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Insert booking
        cursor.execute("""
            INSERT INTO bookings
            (
                pnr,
                train_id,
                passenger_name,
                age,
                gender,
                phone,
                email,
                source,
                destination,
                journey_date,
                class_type,
                seat_count,
                seat_numbers,
                fare_per_seat,
                total_fare,
                booking_status,
                booking_time
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            pnr,
            train_id,
            passenger_name,
            age,
            gender,
            phone,
            email,
            source,
            destination,
            journey_date,
            class_type,
            seat_count,
            seat_numbers,
            fare_per_seat,
            total_fare,
            "CONFIRMED",
            booking_time
        ))

        # Reduce available seats
        cursor.execute("""
            UPDATE train_seats
            SET available_seats =
                available_seats - ?
            WHERE train_id = ?
            AND travel_date = ?
            AND class_type = ?
        """, (
            seat_count,
            train_id,
            journey_date,
            class_type
        ))

        conn.commit()

        return {
            "pnr": pnr,
            "seat_numbers": seat_numbers,
            "fare_per_seat": fare_per_seat,
            "total_fare": total_fare
        }, None

    except Exception as e:

        conn.rollback()

        return None, str(e)

    finally:

        conn.close()


def search_booking(pnr):

    conn = get_connection()

    booking = conn.execute("""
        SELECT
            b.*,
            t.train_number,
            t.train_name,
            t.departure_time,
            t.arrival_time,
            t.duration
        FROM bookings b
        INNER JOIN trains t
        ON b.train_id = t.train_id
        WHERE b.pnr = ?
    """, (pnr,)).fetchone()

    conn.close()

    return booking


def get_all_bookings():

    conn = get_connection()

    bookings = conn.execute("""
        SELECT
            b.pnr,
            b.passenger_name,
            b.age,
            b.gender,
            b.phone,
            b.source,
            b.destination,
            b.journey_date,
            b.class_type,
            b.seat_count,
            b.seat_numbers,
            b.total_fare,
            b.booking_status,
            b.booking_time,
            t.train_number,
            t.train_name
        FROM bookings b
        INNER JOIN trains t
        ON b.train_id = t.train_id
        ORDER BY b.booking_id DESC
    """).fetchall()

    conn.close()

    return bookings


def cancel_booking(pnr):

    conn = get_connection()

    try:

        conn.execute("BEGIN IMMEDIATE")

        booking = conn.execute("""
            SELECT *
            FROM bookings
            WHERE pnr = ?
        """, (pnr,)).fetchone()

        if booking is None:

            conn.rollback()

            return False, "Booking not found."

        if booking["booking_status"] == "CANCELLED":

            conn.rollback()

            return False, "Booking is already cancelled."

        # Restore seats
        conn.execute("""
            UPDATE train_seats
            SET available_seats =
                available_seats + ?
            WHERE train_id = ?
            AND travel_date = ?
            AND class_type = ?
        """, (
            booking["seat_count"],
            booking["train_id"],
            booking["journey_date"],
            booking["class_type"]
        ))

        # Update booking status
        conn.execute("""
            UPDATE bookings
            SET booking_status = 'CANCELLED'
            WHERE pnr = ?
        """, (pnr,))

        conn.commit()

        return True, "Booking cancelled successfully."

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        font-size:60px;
        margin-bottom:5px;
    ">
    🚆
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Railway Reservation")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎫 Book Ticket",
        "🔎 Search Booking",
        "❌ Cancel Booking",
        "📋 All Bookings"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Railway Reservation Management System"
)

st.sidebar.caption(
    "Powered by Python + Streamlit + SQLite3"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🚆 Railway Reservation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Book, search and manage railway reservations from one application.'
        '</div>',
        unsafe_allow_html=True
    )

    bookings = get_all_bookings()

    total_bookings = len(bookings)

    confirmed = sum(
        1
        for b in bookings
        if b["booking_status"] == "CONFIRMED"
    )

    cancelled = sum(
        1
        for b in bookings
        if b["booking_status"] == "CANCELLED"
    )

    total_revenue = sum(
        b["total_fare"]
        for b in bookings
        if b["booking_status"] == "CONFIRMED"
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Bookings",
            total_bookings
        )

    with col2:
        st.metric(
            "Confirmed",
            confirmed
        )

    with col3:
        st.metric(
            "Cancelled",
            cancelled
        )

    with col4:
        st.metric(
            "Revenue",
            f"₹{total_revenue:,.2f}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">System Features</div>',
        unsafe_allow_html=True
    )

    feature_cols = st.columns(3)

    with feature_cols[0]:

        st.markdown("""
        ### 🎫 Ticket Booking

        Enter passenger details, select train,
        class and seats. Fare is calculated
        automatically.
        """)

    with feature_cols[1]:

        st.markdown("""
        ### 🔎 Booking Search

        Search an existing booking using
        its unique PNR number.
        """)

    with feature_cols[2]:

        st.markdown("""
        ### ❌ Cancellation

        Cancel a confirmed ticket and
        automatically restore seats.
        """)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BOOK TICKET
# ============================================================

elif page == "🎫 Book Ticket":

    st.markdown(
        '<div class="main-title">🎫 Book Railway Ticket</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Enter passenger and journey information below.'
        '</div>',
        unsafe_allow_html=True
    )

    trains = get_trains()

    # --------------------------------------------------------
    # TRAIN SELECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚆 Journey Details</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        train_options = {
            f"{t['train_number']} - {t['train_name']} "
            f"({t['source']} → {t['destination']})":
            t["train_id"]
            for t in trains
        }

        selected_train_label = st.selectbox(
            "Select Train",
            list(train_options.keys())
        )

        selected_train_id = train_options[
            selected_train_label
        ]

        selected_train = get_train_by_id(
            selected_train_id
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.text_input(
                "Train Number",
                value=selected_train["train_number"],
                disabled=True
            )

        with col2:

            st.text_input(
                "Departure",
                value=(
                    f"{selected_train['source']} "
                    f"at {selected_train['departure_time']}"
                ),
                disabled=True
            )

        with col3:

            st.text_input(
                "Arrival",
                value=(
                    f"{selected_train['destination']} "
                    f"at {selected_train['arrival_time']}"
                ),
                disabled=True
            )

        col1, col2, col3 = st.columns(3)

        with col1:

            journey_date = st.date_input(
                "Journey Date",
                min_value=date.today()
            )

        with col2:

            class_type = st.selectbox(
                "Class",
                [
                    "Sleeper (SL)",
                    "AC 3 Tier (3A)",
                    "AC 2 Tier (2A)",
                    "AC First Class (1A)",
                    "Chair Car (CC)"
                ]
            )

        with col3:

            available = get_available_seats(
                selected_train_id,
                journey_date.isoformat(),
                class_type
            )

            seat_count = st.number_input(
                "Number of Seats",
                min_value=1,
                max_value=max(1, available),
                value=1,
                step=1
            )

        fare_per_seat = get_fare(class_type)

        total_fare = fare_per_seat * seat_count

        fare_col1, fare_col2 = st.columns(2)

        with fare_col1:

            st.info(
                f"Available Seats: **{available}**"
            )

        with fare_col2:

            st.success(
                f"Estimated Fare: **₹{total_fare:,.2f}**"
            )

    # --------------------------------------------------------
    # PASSENGER DETAILS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">👤 Passenger Details</div>',
        unsafe_allow_html=True
    )

    with st.form("booking_form"):

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name *",
                placeholder="Enter full name"
            )

        with col2:

            phone = st.text_input(
                "Mobile Number *",
                placeholder="10-digit mobile number"
            )

        col1, col2, col3 = st.columns(3)

        with col1:

            age = st.number_input(
                "Age *",
                min_value=1,
                max_value=120,
                value=18
            )

        with col2:

            gender = st.selectbox(
                "Gender *",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

        with col3:

            email = st.text_input(
                "Email",
                placeholder="example@gmail.com"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        submit = st.form_submit_button(
            "🎫 Confirm Booking",
            use_container_width=True,
            type="primary"
        )

    if submit:

        # Validation
        if not passenger_name.strip():

            st.error(
                "Please enter passenger name."
            )

        elif not phone.isdigit() or len(phone) != 10:

            st.error(
                "Please enter a valid 10-digit mobile number."
            )

        elif email and "@" not in email:

            st.error(
                "Please enter a valid email address."
            )

        else:

            booking, error = create_booking(
                train_id=selected_train_id,
                passenger_name=passenger_name.strip(),
                age=age,
                gender=gender,
                phone=phone,
                email=email.strip(),
                source=selected_train["source"],
                destination=selected_train["destination"],
                journey_date=journey_date.isoformat(),
                class_type=class_type,
                seat_count=seat_count
            )

            if error:

                st.error(
                    f"Booking failed: {error}"
                )

            else:

                st.balloons()

                st.markdown(
                    f"""
                    <div class="success-card">

                    <h2>✅ Booking Confirmed</h2>

                    <p>Your railway ticket has been
                    successfully booked.</p>

                    <p>PNR Number</p>

                    <div class="pnr">
                    {booking["pnr"]}
                    </div>

                    <hr>

                    <b>Passenger:</b>
                    {passenger_name}<br>

                    <b>Train:</b>
                    {selected_train["train_name"]}
                    ({selected_train["train_number"]})<br>

                    <b>Journey:</b>
                    {selected_train["source"]}
                    → {selected_train["destination"]}<br>

                    <b>Date:</b>
                    {journey_date.strftime("%d-%m-%Y")}<br>

                    <b>Class:</b>
                    {class_type}<br>

                    <b>Seats:</b>
                    {booking["seat_numbers"]}<br>

                    <b>Total Fare:</b>
                    ₹{booking["total_fare"]:,.2f}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# SEARCH BOOKING
# ============================================================

elif page == "🔎 Search Booking":

    st.markdown(
        '<div class="main-title">🔎 Search Booking</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Retrieve your booking using the PNR number.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("search_form"):

        pnr = st.text_input(
            "Enter 10-digit PNR",
            placeholder="Example: 1234567890"
        )

        search = st.form_submit_button(
            "🔎 Search Booking",
            use_container_width=True,
            type="primary"
        )

    if search:

        if not pnr.isdigit() or len(pnr) != 10:

            st.error(
                "Please enter a valid 10-digit PNR."
            )

        else:

            booking = search_booking(pnr)

            if booking is None:

                st.warning(
                    "No booking found for this PNR."
                )

            else:

                status = booking["booking_status"]

                if status == "CONFIRMED":

                    st.success(
                        "Booking Status: CONFIRMED"
                    )

                else:

                    st.error(
                        "Booking Status: CANCELLED"
                    )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Passenger Details")

                    st.write(
                        f"**PNR:** {booking['pnr']}"
                    )

                    st.write(
                        f"**Name:** {booking['passenger_name']}"
                    )

                    st.write(
                        f"**Age:** {booking['age']}"
                    )

                    st.write(
                        f"**Gender:** {booking['gender']}"
                    )

                    st.write(
                        f"**Phone:** {booking['phone']}"
                    )

                    st.write(
                        f"**Email:** {booking['email'] or 'N/A'}"
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Journey Details")

                    st.write(
                        f"**Train:** "
                        f"{booking['train_number']} - "
                        f"{booking['train_name']}"
                    )

                    st.write(
                        f"**From:** {booking['source']}"
                    )

                    st.write(
                        f"**To:** {booking['destination']}"
                    )

                    st.write(
                        f"**Journey Date:** "
                        f"{booking['journey_date']}"
                    )

                    st.write(
                        f"**Class:** "
                        f"{booking['class_type']}"
                    )

                    st.write(
                        f"**Seats:** "
                        f"{booking['seat_numbers']}"
                    )

                    st.write(
                        f"**Total Fare:** "
                        f"₹{booking['total_fare']:,.2f}"
                    )

                    st.write(
                        f"**Booking Time:** "
                        f"{booking['booking_time']}"
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


# ============================================================
# CANCEL BOOKING
# ============================================================

elif page == "❌ Cancel Booking":

    st.markdown(
        '<div class="main-title">❌ Cancel Booking</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Cancel an existing confirmed reservation.'
        '</div>',
        unsafe_allow_html=True
    )

    pnr = st.text_input(
        "Enter PNR Number",
        placeholder="Enter 10-digit PNR"
    )

    if st.button(
        "🔍 Find Booking",
        use_container_width=True
    ):

        if not pnr.isdigit() or len(pnr) != 10:

            st.error(
                "Please enter a valid 10-digit PNR."
            )

        else:

            booking = search_booking(pnr)

            if booking is None:

                st.error(
                    "Booking not found."
                )

            else:

                st.session_state["cancel_pnr"] = pnr
                st.session_state["cancel_booking"] = dict(
                    booking
                )

    if "cancel_booking" in st.session_state:

        booking = st.session_state[
            "cancel_booking"
        ]

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("Booking Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**PNR:** {booking['pnr']}"
            )

            st.write(
                f"**Passenger:** "
                f"{booking['passenger_name']}"
            )

        with col2:

            st.write(
                f"**Train:** "
                f"{booking['train_name']}"
            )

            st.write(
                f"**Journey Date:** "
                f"{booking['journey_date']}"
            )

        with col3:

            st.write(
                f"**Seats:** "
                f"{booking['seat_numbers']}"
            )

            st.write(
                f"**Fare:** "
                f"₹{booking['total_fare']:,.2f}"
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        if booking["booking_status"] == "CONFIRMED":

            confirm = st.checkbox(
                "I confirm that I want to cancel this booking."
            )

            if st.button(
                "❌ Cancel Ticket",
                type="primary",
                disabled=not confirm,
                use_container_width=True
            ):

                success, message = cancel_booking(
                    booking["pnr"]
                )

                if success:

                    st.success(message)

                    del st.session_state[
                        "cancel_booking"
                    ]

                    st.rerun()

                else:

                    st.error(message)

        else:

            st.warning(
                "This booking is already cancelled."
            )


# ============================================================
# ALL BOOKINGS
# ============================================================

elif page == "📋 All Bookings":

    st.markdown(
        '<div class="main-title">📋 All Bookings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View booking records stored in SQLite database.'
        '</div>',
        unsafe_allow_html=True
    )

    bookings = get_all_bookings()

    if not bookings:

        st.info(
            "No bookings are available."
        )

    else:

        import pandas as pd

        data = []

        for booking in bookings:

            data.append({
                "PNR": booking["pnr"],
                "Passenger": booking["passenger_name"],
                "Age": booking["age"],
                "Gender": booking["gender"],
                "Phone": booking["phone"],
                "Train": (
                    f"{booking['train_number']} - "
                    f"{booking['train_name']}"
                ),
                "From": booking["source"],
                "To": booking["destination"],
                "Journey Date": booking["journey_date"],
                "Class": booking["class_type"],
                "Seats": booking["seat_numbers"],
                "Fare": f"₹{booking['total_fare']:,.2f}",
                "Status": booking["booking_status"],
                "Booking Time": booking["booking_time"]
            })

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="⬇️ Download Booking Records",
            data=df.to_csv(index=False),
            file_name="railway_bookings.csv",
            mime="text/csv",
            use_container_width=True
        )