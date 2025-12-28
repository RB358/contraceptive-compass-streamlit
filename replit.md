# Contraception Finder App

## Overview

A Streamlit-based web application designed to help women understand their contraception choices and select a method tailored to their individual needs. The app presents a quiz-style interface that asks users about their health conditions, preferences, and priorities, then provides personalized recommendations from a curated database of contraceptive methods.

The application categorizes recommendations into three tiers: recommended methods (best match for user's criteria), caution methods (may work but have considerations), and contraindicated methods (not suitable based on health factors).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Framework**: Streamlit (v1.30+)
- **Language**: Python
- **Rationale**: Streamlit provides rapid prototyping for data-driven web apps with minimal frontend code, ideal for quiz-style medical decision support tools

### Core Module Structure
The application follows a modular architecture within the `core/` package:

| Module | Purpose |
|--------|---------|
| `methods_data.py` | Static data store for contraceptive methods and telehealth options |
| `schema.py` | Question definitions and answer encoding logic |
| `quiz_logic.py` | Recommendation engine with medical contraindication rules |
| `render_helpers.py` | HTML/Markdown formatting utilities for display |

### Recommendation Engine Design
- **Pattern**: Rule-based filtering with priority matching
- **Medical Safety Logic**: Methods are flagged as contraindicated based on user health conditions (smoking, blood clots, migraines, high blood pressure, breastfeeding status)
- **Priority Matching**: User preferences (effectiveness, hormone-free, period management, low maintenance, fertility return) influence which methods are marked as "recommended"

### Data Model
Contraceptive methods are stored as dictionaries with:
- Effectiveness rates (perfect vs typical use)
- Hormone type classification
- Pros/cons lists
- Failure rate percentages for sorting/filtering

### Frontend Architecture
- Single-page Streamlit application (`streamlit_app.py`)
- Hero image with CSS overlay styling
- Session state management for quiz flow
- Base64-encoded local images for reliable asset loading

## External Dependencies

### Python Packages
| Package | Purpose |
|---------|---------|
| `streamlit` | Web application framework |
| `pandas` | Data manipulation (available but minimally used currently) |

### Assets
- Local image assets stored in `Assets/` directory
- External image URLs for contraceptive method cards (hosted on healthline.com, self.com, plannedparenthood.org)

### Telehealth Integration
- `TELEHEALTH_OPTIONS` in `methods_data.py` contains links to external telehealth services
- Integration is link-based (no API calls), directing users to third-party consultation platforms

### Database
- No database currently implemented
- All data is stored in-memory via Python dictionaries in `methods_data.py`
- Future consideration: Could add persistence for user preferences or analytics