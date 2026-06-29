# RPN Calculator with Visual Stack Trace

A Python-based GUI calculator that demonstrates **Reverse Polish Notation (RPN)** using a real-time stack visualizer.

## Overview

This project implements a fully functional RPN calculator using **Python** and **Flet**, a Flutter-powered Python framework for building interactive user interfaces.

Unlike a normal calculator, an RPN calculator uses postfix notation, where operators come after operands. For example:

```text
3 4 +
```

This means:

```text
3 + 4 = 7
```

The main goal of this project is not only to calculate results, but also to help users understand how a **stack data structure** works internally.

## Key Features

- Visual stack display showing push and pop operations in real time
- Step-by-step execution mode for learning RPN logic
- Basic arithmetic operations: addition, subtraction, multiplication, and division
- Advanced stack operations such as `SWAP` and `ROT`
- Keyboard support for faster input
- Error handling for division by zero and stack underflow
- Simple GUI built with Flet

## Technology Stack

| Area | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| GUI Framework | Flet |
| UI Foundation | Flutter-powered interface through Flet |
| Core Concept | Stack data structure, LIFO |

## Project Structure

```text
RPNCalculator/
├── src/
│   └── rpn_calculator/
│       ├── __init__.py
│       └── app.py
├── docs/
│   ├── report/
│   │   └── RPNCalculator.pdf
│   └── presentation/
│       └── PDFtex.tex
├── assets/
│   └── images/
│       ├── hp35.jpg
│       └── stack_plates.jpg
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/RPNCalculator.git
cd RPNCalculator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python src/rpn_calculator/app.py
```

## Example Usage

Enter the expression:

```text
3 4 + 5 *
```

Execution flow:

```text
3 4 + = 7
7 5 * = 35
```

Final result:

```text
35
```

## Learning Outcome

This project demonstrates how stack-based calculation works and how data structures can be visualized through a graphical user interface. It is useful for understanding:

- Reverse Polish Notation
- Stack operations
- GUI event handling
- Step-by-step algorithm execution
- Basic software documentation and project structuring

## Authors

- Gautam Ramesh
- Subash Karapparambu Suresh Kumar

## License

This project is intended for academic and learning purposes. Add a license if you plan to publish it as an open-source project.
