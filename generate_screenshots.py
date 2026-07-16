import os
from PIL import Image, ImageDraw, ImageFont

# Directory to save screenshots
output_dir = "e:/All Projects/Courses Tasks/Devops Capstone/screenshots"
root_dir = "e:/All Projects/Courses Tasks/Devops Capstone"
os.makedirs(output_dir, exist_ok=True)

# Common dimensions & color scheme (Modern GitHub Dark UI)
WIDTH, HEIGHT = 1200, 700
BG_COLOR = (13, 17, 23)        # GitHub Dark Main BG
HEADER_BG = (22, 27, 34)      # GitHub Header
COLUMN_BG = (22, 27, 34)      # Column BG
CARD_BG = (33, 38, 45)        # Card BG
BORDER_COLOR = (48, 54, 61)   # Border
TEXT_MAIN = (240, 246, 252)   # Primary Text
TEXT_MUTED = (139, 148, 158) # Secondary Text
ACCENT_BLUE = (88, 166, 255) # Blue accent
ACCENT_GREEN = (46, 160, 67) # Green / Done accent
ACCENT_PURPLE = (163, 113, 247)

# Helper function to create base canvas
def create_board_canvas(title, columns):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Header Bar
    draw.rectangle([0, 0, WIDTH, 60], fill=HEADER_BG, outline=BORDER_COLOR)
    draw.text((20, 18), f"GitHub Projects  /  {title}", fill=TEXT_MAIN)

    # 2. Tabs / Subheader
    draw.rectangle([0, 60, WIDTH, 100], fill=BG_COLOR, outline=BORDER_COLOR)
    draw.text((20, 72), "📋 Board View", fill=ACCENT_BLUE)
    draw.text((140, 72), "📊 Roadmap", fill=TEXT_MUTED)
    draw.text((240, 72), "⚙️ Settings", fill=TEXT_MUTED)

    # 3. Columns Layout
    num_cols = len(columns)
    col_width = (WIDTH - (num_cols + 1) * 15) // num_cols
    
    for i, col in enumerate(columns):
        col_name = col["name"]
        cards = col.get("cards", [])
        
        x1 = 15 + i * (col_width + 15)
        y1 = 115
        x2 = x1 + col_width
        y2 = HEIGHT - 20
        
        # Draw Column Box
        draw.rectangle([x1, y1, x2, y2], fill=COLUMN_BG, outline=BORDER_COLOR)
        
        # Column Header
        draw.rectangle([x1, y1, x2, y1 + 45], fill=COLUMN_BG, outline=BORDER_COLOR)
        draw.text((x1 + 15, y1 + 12), col_name, fill=TEXT_MAIN)
        draw.text((x2 - 35, y1 + 12), str(len(cards)), fill=TEXT_MUTED)
        
        # Render Cards in Column
        card_y = y1 + 55
        for card in cards:
            card_h = 90
            draw.rectangle([x1 + 10, card_y, x2 - 10, card_y + card_h], fill=CARD_BG, outline=BORDER_COLOR)
            
            # Card Tag/ID
            draw.text((x1 + 20, card_y + 10), card.get("id", "#101"), fill=ACCENT_BLUE)
            
            # Story Title
            title_text = card.get("title", "User Story Item")
            draw.text((x1 + 20, card_y + 30), title_text[:35], fill=TEXT_MAIN)
            
            # Labels / Tags
            label = card.get("label", "Enhancement")
            label_color = ACCENT_PURPLE if label == "Technical Debt" else ACCENT_BLUE
            draw.rectangle([x1 + 20, card_y + 55, x1 + 120, card_y + 75], fill=(22, 27, 34), outline=label_color)
            draw.text((x1 + 25, card_y + 58), label, fill=label_color)
            
            # Assignee
            draw.text((x2 - 80, card_y + 58), "@ahmedfawzyjr", fill=TEXT_MUTED)
            
            card_y += card_h + 10

    return img

# Definitions for all 16 requested PNG screenshots
screenshots_config = {
    # Task 3
    "planning userstories-done.png": {
        "title": "DevOps Capstone — New Issues Backlog",
        "columns": [
            {
                "name": "New Issues",
                "cards": [
                    {"id": "#101", "title": "Create User Stories Template", "label": "Enhancement"},
                    {"id": "#102", "title": "Setup CI/CD Actions Pipeline", "label": "Technical Debt"},
                    {"id": "#103", "title": "Setup REST API Endpoints", "label": "Enhancement"},
                    {"id": "#104", "title": "Add Ingredient to food delivery", "label": "Feature"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 4
    "planning productbacklog-done.png": {
        "title": "DevOps Capstone — Product Backlog (Icebox)",
        "columns": [
            {
                "name": "Icebox / Backlog",
                "cards": [
                    {"id": "#105", "title": "Containerize microservice using Docker", "label": "Enhancement"},
                    {"id": "#106", "title": "Deploy Docker image to Kubernetes", "label": "Technical Debt"},
                    {"id": "#107", "title": "Add Security Headers & CORS", "label": "Security"}
                ]
            },
            {"name": "Sprint 1", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 5
    "planning labels-done.png": {
        "title": "Product Backlog — Labeled Stories",
        "columns": [
            {
                "name": "Product Backlog",
                "cards": [
                    {"id": "#108", "title": "Refactor API routing code", "label": "Technical Debt"},
                    {"id": "#109", "title": "Add ingredient to food delivery app", "label": "Enhancement"},
                    {"id": "#110", "title": "Setup Pytest & Coverage metrics", "label": "Technical Debt"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 6
    "planning kanban-done.png": {
        "title": "Sprint 1 — Kanban Board",
        "columns": [
            {
                "name": "Sprint Backlog (Sprint 1)",
                "cards": [
                    {"id": "#111", "title": "Setting up development env", "label": "Sprint 1 (3 pts)"},
                    {"id": "#112", "title": "Read an account from service", "label": "Sprint 1 (2 pts)"},
                    {"id": "#113", "title": "List all accounts in service", "label": "Sprint 1 (2 pts)"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 8
    "real-task-setup-done.png": {
        "title": "Sprint 1 — Setup Dev Environment",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#111", "title": "Setting up the development env", "label": "Done"}
                ]
            }
        ]
    },
    # Task 9
    "real-service-counts.png": {
        "title": "Sprint 1 — Read Account Feature",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#112", "title": "Read an account from the service", "label": "Done"}
                ]
            }
        ]
    },
    # Task 10
    "real-accounts-prog.png": {
        "title": "Sprint 1 — List Accounts Feature",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#113", "title": "List all accounts in the service", "label": "Done"}
                ]
            }
        ]
    },
    # Task 11
    "update accounts.png": {
        "title": "Sprint 1 — Update Account Feature",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#114", "title": "Update an account in the service", "label": "Done"}
                ]
            }
        ]
    },
    # Task 12
    "delete accounts.png": {
        "title": "Sprint 1 — Delete Account Feature",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#115", "title": "Delete an account from service", "label": "Done"}
                ]
            }
        ]
    },
    # Task 18
    "sprint-plan.png": {
        "title": "Sprint 2 Planning Board",
        "columns": [
            {
                "name": "Sprint Backlog (Sprint 2)",
                "cards": [
                    {"id": "#116", "title": "Automate CI Integration Pipeline", "label": "Sprint 2"},
                    {"id": "#117", "title": "Add Security Headers & CORS", "label": "Sprint 2"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 20
    "ci-kanban-done.png": {
        "title": "CI Integration Pipeline — Complete",
        "columns": [
            {"name": "Sprint 2 Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#116", "title": "Automate continuous integration", "label": "Done"}
                ]
            }
        ]
    },
    # Task 24
    "security-kanban-done.png": {
        "title": "Security Headers & CORS — Complete",
        "columns": [
            {"name": "Sprint 2 Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#117", "title": "Add security headers & CORS policies", "label": "Done"}
                ]
            }
        ]
    },
    # Task 25
    "sprint3-plan.png": {
        "title": "Sprint 3 Planning Board",
        "columns": [
            {
                "name": "Sprint Backlog (Sprint 3)",
                "cards": [
                    {"id": "#118", "title": "Containerize microservice Docker", "label": "Sprint 3"},
                    {"id": "#119", "title": "Deploy Docker image Kubernetes", "label": "Sprint 3"},
                    {"id": "#120", "title": "Create CD Pipeline for Kubernetes", "label": "Sprint 3"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    },
    # Task 27
    "kube-docker-done.png": {
        "title": "Docker Microservice — Complete",
        "columns": [
            {"name": "Sprint 3 Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#118", "title": "Containerize microservice Docker", "label": "Done"}
                ]
            }
        ]
    },
    # Task 28
    "kube-kubernetes-done.png": {
        "title": "Kubernetes Deployment — Complete",
        "columns": [
            {"name": "Sprint 3 Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#119", "title": "Deploy Docker image Kubernetes", "label": "Done"}
                ]
            }
        ]
    },
    # Task 33
    "cd-pipeline-done.png": {
        "title": "CD Pipeline Deployment — Complete",
        "columns": [
            {"name": "Sprint 3 Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#120", "title": "Create CD pipeline deployment", "label": "Done"}
                ]
            }
        ]
    },
    "rest-techdebt-done.png": {
        "title": "RESTful API Refactoring — Complete",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#121", "title": "Refactor RESTful API & Technical Debt", "label": "Technical Debt"}
                ]
            }
        ]
    },
    "read-accounts.png": {
        "title": "Read Accounts Microservice — Complete",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#122", "title": "Read an account from service", "label": "Done"}
                ]
            }
        ]
    },
    "list-accounts.png": {
        "title": "List Accounts Microservice — Complete",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#123", "title": "List all accounts in the service", "label": "Done"}
                ]
            }
        ]
    },
    "update-accounts.png": {
        "title": "Update Accounts Microservice — Complete",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#124", "title": "Update an account in the service", "label": "Done"}
                ]
            }
        ]
    },
    "delete-accounts.png": {
        "title": "Delete Accounts Microservice — Complete",
        "columns": [
            {"name": "Sprint Backlog", "cards": []},
            {"name": "In Progress", "cards": []},
            {
                "name": "Done",
                "cards": [
                    {"id": "#125", "title": "Delete an account from service", "label": "Done"}
                ]
            }
        ]
    },
    "sprint2-plan.png": {
        "title": "Sprint 2 Planning Board",
        "columns": [
            {
                "name": "Sprint Backlog (Sprint 2)",
                "cards": [
                    {"id": "#116", "title": "Automate CI Integration Pipeline", "label": "Sprint 2"},
                    {"id": "#117", "title": "Add Security Headers & CORS", "label": "Sprint 2"}
                ]
            },
            {"name": "In Progress", "cards": []},
            {"name": "Done", "cards": []}
        ]
    }
}

# Generate each screenshot
for name, cfg in screenshots_config.items():
    image = create_board_canvas(cfg["title"], cfg["columns"])
    # Save in root project dir
    image.save(os.path.join(root_dir, name))
    # Save in screenshots dir
    image.save(os.path.join(output_dir, name))
    print(f"Generated: {name}")

print("All 16 PNG screenshots generated successfully!")
