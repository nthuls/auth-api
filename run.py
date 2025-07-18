from app import create_app, db

app = create_app()

# Initialize the database
with app.app_context():
    db.create_all()
    
    # Print all registered routes
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} ({rule.endpoint})")

if __name__ == "__main__":
    app.run(debug=True)