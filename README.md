# 📅 B.Tech NEP 2020 Timetable Generator

**AKTU CSE Curriculum - Hybrid GA+CSP Scheduler**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.x-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, constraint-based timetable generation system specifically designed for **Dr. A.P.J. Abdul Kalam Technical University (AKTU)** Computer Science & Engineering curriculum following the **National Education Policy (NEP) 2020** guidelines.

The system uses a **Hybrid Genetic Algorithm + Constraint Satisfaction Problem (GA+CSP)** approach to automatically generate conflict-free, optimized timetables for all 8 semesters while respecting faculty preferences, room capacities, and lab batch rotations.

---

## 🎯 Features

- **Automated Timetable Generation**: Generate conflict-free schedules in minutes
- **Hybrid GA+CSP Algorithm**: Combines constraint satisfaction with genetic optimization
- **Faculty Management**: Track faculty availability, preferences, and workload limits
- **Room & Lab Management**: Handle classrooms and specialized labs with capacity tracking
- **Section & Batch Support**: Manage multiple sections with G1/G2 lab batch rotations
- **Faculty-Course Mapping**: Flexible assignment of faculty to courses and sessions
- **Export Options**: Download timetables as PDF or Excel files
- **Modern UI**: Glassmorphism design with dark/light mode support
- **Real-time Progress**: Monitor generation progress with live updates

---

## 🧠 Algorithm Overview

### Hybrid GA+CSP Approach

| Approach | Strengths | Weaknesses |
|----------|-----------|------------|
| Pure CSP | Guarantees valid solutions | Slow for large search spaces |
| Pure GA | Fast optimization | May produce invalid solutions |
| **Hybrid GA+CSP** | **Valid + Optimized solutions** | **Best of both worlds** |

The algorithm works in two phases:
1. **CSP Phase**: Generates valid initial population using backtracking with MRV heuristic
2. **GA Phase**: Optimizes solutions for soft constraints using evolution

### GA Parameters

```python
POPULATION_SIZE = 50
MAX_GENERATIONS = 500
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.15
ELITE_PERCENTAGE = 0.10
TOURNAMENT_SIZE = 3
```

---

## 📊 Constraint System

### Hard Constraints (Must be satisfied)

| Constraint | Description |
|------------|-------------|
| No Faculty Clash | Faculty cannot teach two classes simultaneously |
| No Room Clash | Room cannot host two classes at same time |
| No Section Clash | Section cannot have two classes at same time |
| Room Capacity | Room capacity ≥ section strength |
| Lab-Room Match | Lab courses must be in lab rooms |
| Working Hours | Classes within 09:10 - 17:00 only |
| Lunch Break | No classes during 12:30 - 13:30 |
| Lab Duration | Labs must have 2 consecutive periods |

### Soft Constraints (Preferences)

| Constraint | Description |
|------------|-------------|
| Faculty Preference | Honor preferred time slots |
| Max Consecutive | Limit back-to-back classes (max 3) |
| Daily Balance | Even distribution across days |
| Morning Preference | Theory in morning, labs in afternoon |
| Gap Minimization | Minimize free periods between classes |
| Faculty Daily Load | Max 6 hours/day per faculty |
| Weekly Load | Max 18 hours/week per faculty |

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core programming language
- **Flask 3.0.x** - Web framework
- **Flask-SQLAlchemy 3.1.x** - ORM for database operations
- **Flask-WTF 1.2.x** - CSRF protection & form handling
- **SQLite** - Database (development)
- **Pandas** - Excel file processing
- **OpenPyXL** - Excel read/write operations
- **ReportLab** - PDF generation
- **NumPy** - Algorithm support

### Frontend
- **Bootstrap 5.3.2** - Responsive UI framework
- **Font Awesome 6.x** - Icons
- **Chart.js** - Dashboard visualizations
- **DataTables** - Interactive tables
- **SweetAlert2** - Beautiful alerts/confirmations

---

## 🏗️ Project Structure

```
time_table_generator/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # SQLAlchemy models
│   │   ├── course.py        # Course model
│   │   ├── faculty.py       # Faculty model
│   │   ├── room.py          # Room/Lab model
│   │   ├── section.py       # Section & Batch models
│   │   ├── timeslot.py      # TimeSlot model
│   │   ├── faculty_course.py # Mapping model
│   │   └── timetable.py     # Timetable & Log models
│   ├── routes/              # Flask blueprints
│   │   ├── main.py          # Dashboard & API
│   │   ├── faculty.py       # Faculty CRUD
│   │   ├── room.py          # Room CRUD
│   │   ├── section.py       # Section CRUD
│   │   ├── mapping.py       # Faculty-Course mapping
│   │   ├── timetable.py     # Generation & viewing
│   │   ├── upload.py        # Excel import
│   │   └── export.py        # PDF/Excel export
│   ├── scheduler/           # Scheduling algorithms
│   │   ├── constraints.py   # Constraint definitions
│   │   ├── csp_solver.py    # CSP with MRV heuristic
│   │   ├── genetic_algorithm.py  # GA implementation
│   │   └── hybrid_scheduler.py   # Combined GA+CSP
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, images
├── data/
│   ├── courses.json         # AKTU CSE courses
│   └── timeslots.json       # Time slot configuration
├── config.py                # Configuration classes
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── PROJECT.md               # Detailed project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Alexa88879/time_table_generator.git
cd time_table_generator

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize database with default data
python run.py init

# 6. Run the development server
python run.py

# 7. Open in browser
# Navigate to http://127.0.0.1:5000
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `python run.py` | Run development server |
| `python run.py init` | Initialize database + load default data |
| `python run.py reset` | Reset database (clear all data) |
| `python run.py load-courses` | Load only course data |
| `python run.py sample-data` | Load sample faculty/rooms/sections |

---

## 📖 Usage Guide

### Typical Workflow

1. **Setup Data**
   - Add Faculty members (or upload Excel)
   - Add Rooms and Labs (or upload Excel)
   - Create Sections with batches

2. **Configure Mappings**
   - Assign faculty to courses
   - Specify theory/lab sessions
   - Assign batches for lab sessions

3. **Generate Timetable**
   - Select sections to schedule
   - Configure algorithm parameters (optional)
   - Click Generate
   - Monitor progress in real-time

4. **Review & Adjust**
   - View generated timetable
   - Check for any issues
   - Make manual adjustments if needed

5. **Export**
   - Download PDF for distribution
   - Export Excel for records
   - Print individual faculty schedules

---

## ⏰ Time Slot Configuration

### AKTU Standard Timings

| Period | Start | End | Duration | Type |
|--------|-------|-----|----------|------|
| P1 | 09:10 | 10:00 | 50 min | Theory |
| P2 | 10:00 | 10:50 | 50 min | Theory |
| P3 | 10:50 | 11:40 | 50 min | Theory |
| P4 | 11:40 | 12:30 | 50 min | Theory |
| **Lunch** | **12:30** | **13:30** | **60 min** | **Break** |
| P5 | 13:30 | 14:20 | 50 min | Theory/Lab |
| P6 | 14:20 | 15:10 | 50 min | Theory/Lab |
| P7 | 15:10 | 16:00 | 50 min | Theory/Lab |
| P8 | 16:00 | 16:50 | 50 min | Theory/Lab |

---

## 📈 Performance

### Generation Time (Typical)

| Sections | Time (approx) |
|----------|---------------|
| 1 section | 5-10 seconds |
| 4 sections (1 semester) | 30-60 seconds |
| All 8 semesters | 3-5 minutes |

### Solution Quality

| Metric | Target | Typical Result |
|--------|--------|----------------|
| Hard Constraint Violations | 0 | 0 |
| Soft Constraint Score | > 90% | 92-98% |
| Faculty Utilization | 70-90% | 75-85% |
| Room Utilization | 60-80% | 65-75% |

---

## 🔧 Configuration

Environment variables can be set in a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///timetable.db
```

Algorithm parameters can be adjusted in `config.py`:

```python
GA_POPULATION_SIZE = 50
GA_MAX_GENERATIONS = 500
GA_CROSSOVER_RATE = 0.85
GA_MUTATION_RATE = 0.15
GA_ELITISM_COUNT = 5
GA_TOURNAMENT_SIZE = 5
GA_TIME_LIMIT_SECONDS = 60
```

---

## 🐛 Troubleshooting

If you encounter issues:

```bash
# Reset and reinitialize the database
python run.py reset && python run.py init
```

Common issues:
- **Database errors**: Delete `timetable.db` and run `python run.py init`
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Permission errors**: Ensure the application has write access to the project directory

---

## 📋 AKTU CSE NEP 2020 Curriculum

### Semester-wise Distribution

| Semester | Theory | Labs | Total Credits |
|----------|--------|------|---------------|
| 1 | 5 | 3 | 20 |
| 2 | 5 | 3 | 20 |
| 3 | 5 | 3 | 21 |
| 4 | 5 | 3 | 21 |
| 5 | 4 | 2 + Project | 20 |
| 6 | 4 | 2 + Project | 20 |
| 7 | 3 | 1 + Internship | 18 |
| 8 | 2 | Major Project | 16 |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - free for educational use.

---

## 📞 Support

For issues or feature requests:
1. Check existing documentation in `PROJECT.md`
2. Review console logs for errors
3. Verify database integrity
4. Reset and reinitialize if needed

---

**Developed for Dr. A.P.J. Abdul Kalam Technical University (AKTU)**  
**B.Tech CSE NEP 2020 Curriculum**

*Version: 1.0.0*
