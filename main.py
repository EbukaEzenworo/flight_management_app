

import sqlite3
import pathlib


DB_NAME = 'FlightManagement.db' # Below is the DataBase name.

# Seed data into the DataBase.
SCHEMA_AND_SEED_SQL = """
PRAGMA foreign_keys = ON;


DROP TABLE IF EXISTS FlightPilot;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS Pilot;
DROP TABLE IF EXISTS Aircraft;
DROP TABLE IF EXISTS Destination;
DROP TABLE IF EXISTS FlightStatus;


CREATE TABLE IF NOT EXISTS Destination (
    destination_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_code        TEXT NOT NULL UNIQUE,
    airport_name        TEXT NOT NULL,
    city                TEXT NOT NULL,
    country             TEXT NOT NULL,
    timezone            TEXT,
    is_active           INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);


CREATE TABLE IF NOT EXISTS Aircraft (
    aircraft_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no     TEXT NOT NULL UNIQUE,
    model               TEXT NOT NULL,
    manufacturer        TEXT NOT NULL,
    seat_capacity       INTEGER NOT NULL CHECK (seat_capacity > 0),
    status              TEXT NOT NULL CHECK (status IN ('Active', 'Maintenance', 'Retired'))
);


CREATE TABLE IF NOT EXISTS Pilot (
    pilot_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    license_no          TEXT NOT NULL UNIQUE,
    first_name          TEXT NOT NULL,
    last_name           TEXT NOT NULL,
    rank                TEXT NOT NULL CHECK (rank IN ('Captain', 'First Officer', 'Relief Pilot')),
    phone               TEXT,
    email               TEXT UNIQUE,
    hire_date           TEXT,
    status              TEXT NOT NULL CHECK (status IN ('Active', 'On Leave', 'Suspended', 'Retired'))
);


CREATE TABLE IF NOT EXISTS FlightStatus (
    status_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name         TEXT NOT NULL UNIQUE,
    description         TEXT
);


CREATE TABLE IF NOT EXISTS Flight (
    flight_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number           TEXT NOT NULL UNIQUE,
    origin_destination_id   INTEGER NOT NULL,
    arrival_destination_id  INTEGER NOT NULL,
    aircraft_id             INTEGER NOT NULL,
    status_id               INTEGER NOT NULL,
    scheduled_departure     TEXT NOT NULL,
    scheduled_arrival       TEXT NOT NULL,
    gate                    TEXT,
    remarks                 TEXT,
    FOREIGN KEY (origin_destination_id) REFERENCES Destination(destination_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (arrival_destination_id) REFERENCES Destination(destination_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (status_id) REFERENCES FlightStatus(status_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CHECK (origin_destination_id <> arrival_destination_id),
    CHECK (scheduled_arrival > scheduled_departure)
);


CREATE TABLE IF NOT EXISTS FlightPilot (
    flight_pilot_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id            INTEGER NOT NULL,
    pilot_id             INTEGER NOT NULL,
    assignment_role      TEXT NOT NULL CHECK (assignment_role IN ('Captain', 'First Officer', 'Relief Pilot')),
    assigned_at          TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (pilot_id) REFERENCES Pilot(pilot_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (flight_id, pilot_id)
);


INSERT INTO FlightStatus (status_name, description) VALUES
('Scheduled', 'Flight is scheduled and awaiting operational processing'),
('Boarding', 'Passengers are currently boarding the aircraft'),
('Gate Closed', 'Gate is closed and final departure checks are underway'),
('Delayed', 'Flight departure or arrival has been delayed'),
('Departed', 'Aircraft has left the departure airport'),
('In Air', 'Flight is currently airborne'),
('Landed', 'Aircraft has landed at the destination airport'),
('Arrived', 'Flight has arrived and completed taxi procedures'),
('Cancelled', 'Flight has been cancelled'),
('Completed', 'Flight operations and arrival processing are complete');


INSERT INTO Destination (airport_code, airport_name, city, country, timezone, is_active) VALUES
('LHR', 'Heathrow Airport', 'London', 'United Kingdom', 'Europe/London', 1),
('LGW', 'Gatwick Airport', 'London', 'United Kingdom', 'Europe/London', 1),
('MAN', 'Manchester Airport', 'Manchester', 'United Kingdom', 'Europe/London', 1),
('JFK', 'John F. Kennedy International Airport', 'New York', 'United States', 'America/New_York', 1),
('LAX', 'Los Angeles International Airport', 'Los Angeles', 'United States', 'America/Los_Angeles', 1),
('DXB', 'Dubai International Airport', 'Dubai', 'United Arab Emirates', 'Asia/Dubai', 1),
('LOS', 'Murtala Muhammed International Airport', 'Lagos', 'Nigeria', 'Africa/Lagos', 1),
('ABV', 'Nnamdi Azikiwe International Airport', 'Abuja', 'Nigeria', 'Africa/Lagos', 1),
('CDG', 'Charles de Gaulle Airport', 'Paris', 'France', 'Europe/Paris', 1),
('AMS', 'Amsterdam Airport Schiphol', 'Amsterdam', 'Netherlands', 'Europe/Amsterdam', 1);


INSERT INTO Aircraft (registration_no, model, manufacturer, seat_capacity, status) VALUES
('G-ABCD', 'A320', 'Airbus', 180, 'Active'),
('G-EFGH', 'A321', 'Airbus', 220, 'Active'),
('G-IJKL', '737-800', 'Boeing', 189, 'Active'),
('G-MNOP', '787-9', 'Boeing', 290, 'Maintenance'),
('G-QRST', 'A330-300', 'Airbus', 277, 'Active'),
('G-UVWX', 'E190', 'Embraer', 100, 'Active'),
('G-YZAA', '737 MAX 8', 'Boeing', 175, 'Active'),
('G-BBCC', 'A350-900', 'Airbus', 325, 'Active'),
('G-DDEE', 'ATR 72', 'ATR', 72, 'Active'),
('G-FFGG', 'Q400', 'De Havilland', 78, 'Retired');


INSERT INTO Pilot (license_no, first_name, last_name, rank, phone, email, hire_date, status) VALUES
('LIC1001', 'John', 'Smith', 'Captain', '0700000001', 'john.smith@example.com', '2018-01-15', 'Active'),
('LIC1002', 'Mary', 'Brown', 'First Officer', '0700000002', 'mary.brown@example.com', '2019-03-21', 'Active'),
('LIC1003', 'David', 'Johnson', 'Captain', '0700000003', 'david.johnson@example.com', '2017-07-30', 'Active'),
('LIC1004', 'Grace', 'Taylor', 'First Officer', '0700000004', 'grace.taylor@example.com', '2020-11-05', 'On Leave'),
('LIC1005', 'Daniel', 'Wilson', 'Captain', '0700000005', 'daniel.wilson@example.com', '2016-05-17', 'Active'),
('LIC1006', 'Alice', 'Thomas', 'Relief Pilot', '0700000006', 'alice.thomas@example.com', '2021-09-12', 'Active'),
('LIC1007', 'Samuel', 'White', 'First Officer', '0700000007', 'samuel.white@example.com', '2022-02-01', 'Active'),
('LIC1008', 'Helen', 'Moore', 'Captain', '0700000008', 'helen.moore@example.com', '2015-08-19', 'Suspended'),
('LIC1009', 'Victor', 'Hall', 'Relief Pilot', '0700000009', 'victor.hall@example.com', '2021-12-11', 'Active'),
('LIC1010', 'Linda', 'Adams', 'First Officer', '0700000010', 'linda.adams@example.com', '2020-04-23', 'Active');


INSERT INTO Flight (flight_number, origin_destination_id, arrival_destination_id, aircraft_id, status_id, scheduled_departure, scheduled_arrival, gate, remarks) VALUES
('BA101', 1, 4, 8, 1, '2026-06-10 08:00', '2026-06-10 16:00', 'A1', 'Long-haul service'),
('BA102', 4, 1, 8, 1, '2026-06-11 18:30', '2026-06-12 06:30', 'B2', 'Return service'),
('BA201', 1, 7, 5, 4, '2026-06-10 09:30', '2026-06-10 15:45', 'A5', 'Weather monitoring in progress'),
('BA202', 7, 1, 5, 1, '2026-06-12 10:00', '2026-06-12 16:10', 'A6', 'On schedule'),
('EK301', 6, 1, 4, 2, '2026-06-10 07:45', '2026-06-10 12:15', 'C1', 'Boarding in progress'),
('EK302', 1, 6, 4, 1, '2026-06-10 14:00', '2026-06-10 22:15', 'C2', 'Gate opens 45 minutes before departure'),
('AF401', 9, 1, 1, 3, '2026-06-13 06:20', '2026-06-13 07:10', 'D4', 'Final checks'),
('AF402', 1, 9, 1, 1, '2026-06-13 09:10', '2026-06-13 10:00', 'D5', 'Morning shuttle'),
('KL501', 10, 3, 6, 5, '2026-06-11 11:00', '2026-06-11 12:30', 'E1', 'Departed on time'),
('VS601', 1, 5, 2, 8, '2026-06-14 15:00', '2026-06-14 23:00', 'F7', 'Arrived early');


INSERT INTO FlightPilot (flight_id, pilot_id, assignment_role, assigned_at) VALUES
(1, 1, 'Captain', '2026-06-01 09:00'),
(1, 2, 'First Officer', '2026-06-01 09:05'),
(2, 3, 'Captain', '2026-06-02 10:00'),
(2, 7, 'First Officer', '2026-06-02 10:05'),
(3, 5, 'Captain', '2026-06-03 08:00'),
(3, 10, 'First Officer', '2026-06-03 08:05'),
(4, 1, 'Captain', '2026-06-04 11:00'),
(4, 2, 'First Officer', '2026-06-04 11:05'),
(5, 3, 'Captain', '2026-06-05 07:00'),
(5, 6, 'Relief Pilot', '2026-06-05 07:05'),
(6, 5, 'Captain', '2026-06-06 12:00'),
(6, 7, 'First Officer', '2026-06-06 12:05'),
(7, 1, 'Captain', '2026-06-07 06:00'),
(8, 2, 'First Officer', '2026-06-07 09:00'),
(9, 9, 'Relief Pilot', '2026-06-08 10:00');
"""


SQL_QUERIES = {
    'insert_flight': """
        INSERT INTO Flight (
            flight_number, origin_destination_id, arrival_destination_id,
            aircraft_id, status_id, scheduled_departure, scheduled_arrival,
            gate, remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
    'view_flights_by_criteria': """
        SELECT
            f.flight_id,
            f.flight_number,
            o.airport_code AS origin_code,
            o.city AS origin_city,
            a.airport_code AS arrival_code,
            a.city AS arrival_city,
            ac.model AS aircraft_model,
            fs.status_name,
            f.scheduled_departure,
            f.scheduled_arrival,
            f.gate,
            f.remarks
        FROM Flight f
        JOIN Destination o ON f.origin_destination_id = o.destination_id
        JOIN Destination a ON f.arrival_destination_id = a.destination_id
        JOIN Aircraft ac ON f.aircraft_id = ac.aircraft_id
        JOIN FlightStatus fs ON f.status_id = fs.status_id
        WHERE (? IS NULL 
               OR o.city LIKE '%' || ? || '%' COLLATE NOCASE
               OR a.city LIKE '%' || ? || '%' COLLATE NOCASE 
               OR o.airport_code LIKE '%' || ? || '%' COLLATE NOCASE
               OR a.airport_code LIKE '%' || ? || '%' COLLATE NOCASE
               )
          AND (? IS NULL OR fs.status_name = ? COLLATE NOCASE)
          AND (? IS NULL OR date(f.scheduled_departure) = date(?))
        ORDER BY f.scheduled_departure;
    """,
    'update_flight_schedule': """
        UPDATE Flight
        SET scheduled_departure = ?,
            scheduled_arrival = ?,
            status_id = ?,
            gate = ?,
            remarks = ?
        WHERE flight_id = ?;
    """,
    'assign_pilot_to_flight': """
        INSERT INTO FlightPilot (flight_id, pilot_id, assignment_role)
        VALUES (?, ?, ?);
    """,
    'view_pilot_schedule': """
        SELECT
            p.pilot_id,
            p.first_name || ' ' || p.last_name AS pilot_name,
            p.rank,
            f.flight_number,
            o.city AS origin_city,
            a.city AS arrival_city,
            fp.assignment_role,
            f.scheduled_departure,
            f.scheduled_arrival,
            fs.status_name
        FROM FlightPilot fp
        JOIN Pilot p ON fp.pilot_id = p.pilot_id
        JOIN Flight f ON fp.flight_id = f.flight_id
        JOIN Destination o ON f.origin_destination_id = o.destination_id
        JOIN Destination a ON f.arrival_destination_id = a.destination_id
        JOIN FlightStatus fs ON f.status_id = fs.status_id
        WHERE p.pilot_id = ?
        ORDER BY f.scheduled_departure;
    """,
    'view_destinations': """
        SELECT destination_id, airport_code, airport_name, city, country, timezone, is_active
        FROM Destination
        ORDER BY city;
    """,
    'update_destination': """
        UPDATE Destination
        SET airport_name = ?,
            city = ?,
            country = ?,
            timezone = ?,
            is_active = ?
        WHERE destination_id = ?;
    """,
    'summary_flights_per_destination': """
        SELECT
            d.destination_id,
            d.airport_code,
            d.city,
            COUNT(f.flight_id) AS total_arrivals
        FROM Destination d
        LEFT JOIN Flight f ON d.destination_id = f.arrival_destination_id
        GROUP BY d.destination_id, d.airport_code, d.city
        ORDER BY total_arrivals DESC, d.city;
    """,
    'summary_flights_per_pilot': """
        SELECT
            p.pilot_id,
            p.first_name || ' ' || p.last_name AS pilot_name,
            p.rank,
            COUNT(fp.flight_id) AS total_flights
        FROM Pilot p
        LEFT JOIN FlightPilot fp ON p.pilot_id = fp.pilot_id
        GROUP BY p.pilot_id, p.first_name, p.last_name, p.rank
        ORDER BY total_flights DESC, pilot_name;
    """,
    'list_statuses': "SELECT status_id, status_name FROM FlightStatus ORDER BY status_id;",
    'list_aircraft': "SELECT aircraft_id, registration_no, model, status FROM Aircraft ORDER BY aircraft_id;",
    'list_destinations': "SELECT destination_id, airport_code, city, country FROM Destination ORDER BY destination_id;",
    'list_pilots': "SELECT pilot_id, first_name || ' ' || last_name AS pilot_name, rank, status FROM Pilot ORDER BY pilot_id;",
    'list_flights': "SELECT flight_id, flight_number FROM Flight ORDER BY flight_id;"
}



# Initialise db connection using sqlite3
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.row_factory = sqlite3.Row
    return conn



# Initialise and run database seed sql script
def initialize_database(conn=None, force_reset=False):
    db_exists = pathlib.Path(DB_NAME).exists()
    if force_reset or not db_exists:
        close_after = False
        if conn is None:
            conn = get_connection()
            close_after = True
        conn.executescript(SCHEMA_AND_SEED_SQL)
        conn.commit()
        if close_after:
            conn.close()
        print('Database created and populated with sample data successfully.')
    else:
        print('Database already exists. Using the existing database.')




def print_rows(rows):
    if not rows:
        print('No records found.')
        return
    headers = list(rows[0].keys())
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(row[h])))
    line = ' | '.join(h.ljust(widths[h]) for h in headers)
    print(line)
    print('-' * len(line))
    for row in rows:
        print(' | '.join(str(row[h]).ljust(widths[h]) for h in headers))
    print()




def fetch_all(conn, query, params=()):
    return conn.execute(query, params).fetchall()




def list_reference_data(conn):
    print('Available Destinations:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_destinations']))
    print('Available Aircraft:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_aircraft']))
    print('Available Flight Statuses:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_statuses']))



# Add new flight data
def add_new_flight(conn):
    print('--- Add a New Flight ---')
    list_reference_data(conn)
    flight_number = input('Enter flight number: ').strip()
    origin_destination_id = int(input('Enter origin destination_id: ').strip())
    arrival_destination_id = int(input('Enter arrival destination_id: ').strip())
    aircraft_id = int(input('Enter aircraft_id: ').strip())
    status_id = int(input('Enter status_id: ').strip())
    scheduled_departure = input('Enter scheduled departure (YYYY-MM-DD HH:MM): ').strip()
    scheduled_arrival = input('Enter scheduled arrival (YYYY-MM-DD HH:MM): ').strip()
    gate = input('Enter gate: ').strip()
    remarks = input('Enter remarks: ').strip()
    conn.execute(SQL_QUERIES['insert_flight'], (
        flight_number, origin_destination_id, arrival_destination_id,
        aircraft_id, status_id, scheduled_departure, scheduled_arrival,
        gate, remarks
    ))
    conn.commit()
    print('Flight added successfully.')



# View flights based on criteria
def view_flights_by_criteria(conn):
    print('--- View Flights by Criteria ---')
    destination = input('Enter destination city or airport code (leave blank for all): It is case insensitive ').strip() or None
    status = input("Enter status name e.g 'Landed','In Air' (leave blank for all): It is case insensitive ").strip() or None
    departure_date = input('Enter departure date YYYY-MM-DD (leave blank for all): ').strip() or None
    rows = fetch_all(conn, SQL_QUERIES['view_flights_by_criteria'], (
        destination, destination, destination, destination, destination,
        status, status,
        departure_date, departure_date
    ))
    print_rows(rows)




def update_flight_information(conn):
    print('--- Update Flight Information ---')
    print_rows(fetch_all(conn, SQL_QUERIES['list_flights']))
    print('Statuses:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_statuses']))
    flight_id = int(input('Enter flight_id to update: ').strip())
    scheduled_departure = input('Enter new departure (YYYY-MM-DD HH:MM): ').strip()
    scheduled_arrival = input('Enter new arrival (YYYY-MM-DD HH:MM): ').strip()
    status_id = int(input('Enter new status_id: ').strip())
    gate = input('Enter new gate: ').strip()
    remarks = input('Enter new remarks: ').strip()
    cur = conn.execute(SQL_QUERIES['update_flight_schedule'], (
        scheduled_departure, scheduled_arrival, status_id, gate, remarks, flight_id
    ))
    conn.commit()
    print(f'{cur.rowcount} flight record(s) updated.')




def assign_pilot_to_flight(conn):
    print('--- Assign Pilot to Flight ---')
    print('Flights:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_flights']))
    print('Pilots:')
    print_rows(fetch_all(conn, SQL_QUERIES['list_pilots']))
    flight_id = int(input('Enter flight_id: ').strip())
    pilot_id = int(input('Enter pilot_id: ').strip())
    assignment_role = input('Enter assignment role (Captain / First Officer / Relief Pilot): ').strip()
    conn.execute(SQL_QUERIES['assign_pilot_to_flight'], (flight_id, pilot_id, assignment_role))
    conn.commit()
    print('Pilot assigned successfully.')




def view_pilot_schedule(conn):
    print('--- View Pilot Schedule ---')
    print_rows(fetch_all(conn, SQL_QUERIES['list_pilots']))
    pilot_id = int(input('Enter pilot_id: ').strip())
    rows = fetch_all(conn, SQL_QUERIES['view_pilot_schedule'], (pilot_id,))
    print_rows(rows)




def manage_destinations(conn):
    print('--- View / Update Destination Information ---')
    rows = fetch_all(conn, SQL_QUERIES['view_destinations'])
    print_rows(rows)
    choice = input('Do you want to update a destination? (y/n): ').strip().lower()
    if choice == 'y':
        destination_id = int(input('Enter destination_id to update: ').strip())
        airport_name = input('Enter new airport name: ').strip()
        city = input('Enter new city: ').strip()
        country = input('Enter new country: ').strip()
        timezone = input('Enter new timezone: ').strip()
        is_active = int(input('Enter is_active (1 for active, 0 for inactive): ').strip())
        cur = conn.execute(SQL_QUERIES['update_destination'], (
            airport_name, city, country, timezone, is_active, destination_id
        ))
        conn.commit()
        print(f'{cur.rowcount} destination record(s) updated.')




def show_summary_reports(conn):
    print('--- Summary Reports ---')
    print('Enter 1 to see the number of flights to each destination')
    print('Enter 2 to see the number of flights assigned to each pilot')
    choice = input('Select report option: ').strip()
    if choice == '1':
        print_rows(fetch_all(conn, SQL_QUERIES['summary_flights_per_destination']))
    elif choice == '2':
        print_rows(fetch_all(conn, SQL_QUERIES['summary_flights_per_pilot']))
    else:
        print('Invalid report option.')




def run_cli():
    with get_connection() as conn:
        initialize_database(conn=conn, force_reset=not pathlib.Path(DB_NAME).exists())
        while True:
            print('========== Flight Management CLI ==========' )
            print('1. Reset database and load sample data')
            print('2. Add a New Flight')
            print('3. View Flights by Criteria')
            print('4. Update Flight Information')
            print('5. Assign Pilot to Flight')
            print('6. View Pilot Schedule')
            print('7. View/Update Destination Information')
            print('8. Summary Reports')
            print('9. Exit')
            choice = input('Choose an option: ').strip()
            try:
                if choice == '1':
                    initialize_database(conn=conn, force_reset=True)
                elif choice == '2':
                    add_new_flight(conn)
                elif choice == '3':
                    view_flights_by_criteria(conn)
                elif choice == '4':
                    update_flight_information(conn)
                elif choice == '5':
                    assign_pilot_to_flight(conn)
                elif choice == '6':
                    view_pilot_schedule(conn)
                elif choice == '7':
                    manage_destinations(conn)
                elif choice == '8':
                    show_summary_reports(conn)
                elif choice == '9':
                    print('Exiting application. Goodbye!')
                    break
                else:
                    print('Invalid option. Please try again.')
            except sqlite3.IntegrityError as exc:
                print(f'Database constraint error: {exc}')
            except ValueError:
                print('Invalid input type. Please enter the correct value format.')
            except Exception as exc:
                print(f'Unexpected error: {exc}')




if __name__ == '__main__':
    run_cli()
